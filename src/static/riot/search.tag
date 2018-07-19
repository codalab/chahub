<search-results>
    <div id="particle_header" class="ui centered grid">
        <div class="ui row">
            <img id="brand_logo" src="static/img/temp_chahub_logo.png">
            <img id="brand_logo_mobile" src="static/img/Chahub_C.png">

            <!-- We keep 1 empty column here to align the brand logo defined above this element -->
            <div class="one wide column"></div>

            <div class="fourteen wide mobile twelve wide tablet nine wide computer column">
                <div class="ui centered grid">
                    <div class="centered row">
                        <div class="ui fourteen wide mobile fifteen wide search-wrapper column">
                            <div id="searchbar" class="ui left action right icon input">
                                <button class="ui icon button" onclick="{ clear_search }">
                                    <i class="delete icon"></i>
                                </button>
                                <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">
                                <i class="search icon"></i>

                                <div id="ellipses" class="mobile only one wide column">
                                    <div class="ui icon button">
                                        <i class="large ellipsis vertical icon"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="centered row">
                        <div id="mobile-friendly-column" class="six wide center aligned column">
                            <div id="mobile-friendly-button" ref="time_filter"
                                 class="ui tiny labeled icon dropdown button">
                                <i class="calendar icon"></i>
                                <span class="text">Any Time</span>
                                <div class="menu">
                                    <div class="header">
                                        Timeframe
                                    </div>
                                    <div class="divider"></div>
                                    <div class="active item" data-value="">
                                        Any Time
                                    </div>
                                    <div class="item" data-value="active">
                                        Active
                                    </div>
                                    <div class="item" data-value="this_month">
                                        Created this month
                                    </div>
                                    <div class="item" data-value="this_year">
                                        Created this year
                                    </div>
                                    <div class="divider"></div>
                                    <div class="header">
                                        Date range
                                    </div>
                                    <div class="ui left icon input datepicker" data-calendar-type="start">
                                        <i class="calendar icon"></i>
                                        <input ref="start_date" type="text" name="search"
                                               placeholder="Start date">
                                    </div>
                                    <div class="ui left icon input datepicker" data-calendar-type="end">
                                        <i class="calendar icon"></i>
                                        <input ref="end_date" type="text" name="search" placeholder="End date">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div id="mobile-friendly-column" class="six wide center aligned column">
                            <div id="mobile-friendly-button" ref="sort_filter"
                                 class="ui tiny labeled icon dropdown button">
                                <i class="filter icon"></i>
                                <span class="text">Relevance</span>
                                <div class="menu">
                                    <div class="header">
                                        Sorting
                                    </div>
                                    <div class="divider"></div>
                                    <div class="active item" data-value="">
                                        Relevance
                                    </div>
                                    <div data-value="deadline" class="item">
                                        Deadline
                                    </div>
                                    <div data-value="prize" class="item">
                                        Prize Amount
                                    </div>
                                    <div data-value="participant_count" class="item">
                                        Participant Count
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div id="mobile-friendly-column" class="four wide center aligned column"
                             show="{!disallow_producer_selection}">
                            <div id="mobile-friendly-button" ref="producer_filter"
                                 class="ui tiny labeled icon dropdown button">
                                <i class="globe icon"></i>
                                <span class="text">All</span>
                                <div class="menu">
                                    <div class="header">
                                        Provider
                                    </div>
                                    <div class="divider"></div>
                                    <div class="active item" data-value="">
                                        All
                                    </div>
                                    <virtual each="{PRODUCERS}">
                                        <div class="item" data-value="{id}">{name}</div>
                                    </virtual>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet computer only one wide column">
                <a id="login-button" hide="{USER_AUTHENTICATED}" style="" href="/accounts/login/"
                   class="ui button">LOGIN</a>
                <a id="login-button" show="{USER_AUTHENTICATED}" style="" href="/accounts/logout/"
                   class="ui button">LOGOUT</a>
            </div>
        </div>
        <div id="mobile_drop" class="sixteen wide mobile only column">
            <button id="down_caret" class="ui icon button" click="{ toggle_search_options }"><i class="down caret icon"></i>Search Options</button>
        </div>
    </div>

    <div show="{ display_search_options }">
        dix
    </div>

    <div id="mobile-grid" class="ui centered grid">
        <div id="mobile" class="fourteen wide column">
            <div class="ui stacked">
                <div class="ui warning message" show="{showing_default_results}">
                    <div class="header">
                        No results found
                    </div>
                    Try broadening your search
                </div>
                <div class="ui middle aligned compact divided link items content-desktop" style="margin-top: 0;">
                    <competition-tile each="{ results }" no-reorder class="item"
                                      style="padding: .5em 0;"></competition-tile>
                </div>
                <div class="ui middle aligned compact link items content-mobile" style="margin-top: -1;">
                    <competition-mobile-tile each="{ results }" no-reorder class="item"
                                             style="padding: -1em;"></competition-mobile-tile>
                </div>
            </div>
        </div>
    </div>

    <script>
        var self = this
        self.results = []
        self.display_mode = 'list'
        self.old_filters = {}
        self.display_search_options = false

        self.on('mount', function () {
            /*$(self.refs.search_wrapper).dropdown({


             on results do


             onNoResults: function(search) {}
             })*/
            // header particles
            particlesJS.load('particle_header', URLS.assets.header_particles)

            // Template stuff
            $('.datepicker').calendar({
                type: 'date',
                formatter: {
                    date: function (date, settings) {
                        return luxon.DateTime.fromJSDate(date).toISODate()
                    }
                },
                popupOptions: {
                    position: 'bottom left',
                    lastResort: 'bottom left',
                    hideOnScroll: false
                },
                onChange: function (date, text, mode) {
                    self.set_time_dropdown_text()

                    self.search()
                }
            })
            $(".ui.dropdown").dropdown({
                onChange: function () {
                    self.search()
                }
            })
            //$(self.refs.time_filter).dropdown('setting', 'onChange', self.search);

            // Search handling
            $(self.refs.search_wrapper).search({
                apiSettings: {
                    url: URLS.API + "query/?q={query}",
                    onResponse: function (data) {
                        // Let riotJS stuff know about updates
                        self.update({
                            results: data.results,
                            suggestions: data.suggestions
                        })

                        // Handle SemanticUI stuff
                        var response = {
                            results: []
                        };
                        $.each(data.suggestions, function (index, item) {
                            response.results.push({
                                title: item.text
                                //description: item.score
                                //url: item.html_url
                            });
                        });
                        return response;
                    }
                },
                cache: false,  // Disabling cache makes results work properly
                showNoResults: false,
                minCharacters: 2,
                duration: 300,
                transition: 'slide down'
            });
        })

        self.toggle_search_options = function() {
            self.display_search_options = !self.display_search_options
            self.update()
        }

        self.set_time_dropdown_text = function () {
            /*if(this.dataset.calendarType === 'start') {
                self.refs.start_date.value = text
            }

            if(this.dataset.calendarType === 'end') {
                self.refs.end_date.value = text
            }*/

            if (self.refs.start_date.value && self.refs.end_date.value) {
                var temp_string = self.refs.start_date.value + ' through ' + self.refs.end_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
            else if (self.refs.start_date.value) {
                var temp_string = 'Starting from ' + self.refs.start_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
            else if (self.refs.end_date.value) {
                var temp_string = 'End by ' + self.refs.end_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
        }


        self.one('route', function () {
            var params = route.query()

            // On page load set search bar to search and execute search if we were given a query
            self.refs.search.value = params.q || ''

            // TODO: set time_filter dropdown selected value
            // TODO: set sort dropdown selected value
            // TODO: set producer dropdown selected value

            // Date flags and ranges
            if (params.date_flags) {
                $(self.refs.time_filter).dropdown('set selected', params.date_flags)
            } else {
                // If no date flags, maybe we have a date range?
                // Initialize time range values and then force it to update
                self.refs.start_date.value = params.start_date || ''
                self.refs.end_date.value = params.end_date || ''

                // Do this AFTER setting the local variables like self.refs.start_date.value, self.refs.end_date.value, etc.
                // so it can set the proper dropdown text
                self.set_time_dropdown_text()
            }

            // Sorting
            $(self.refs.sort_filter).dropdown('set selected', params.sorting)

            // Producers
            $(self.refs.producer_filter).dropdown('set selected', params.producer)
            // For iframes we might want to hide producer selection
            self.disallow_producer_selection = params.disallow_producer_selection

            self.search()

            // Focus on search
            self.refs.search.focus()
        })

        self.input_updated = function () {
            delay(function () {
                self.search()
            }, 250)
        }

        self.clear_search = function () {
            self.refs.search.value = ''
            self.refs.start_date.value = ''
            self.refs.end_date.value = ''
            $(self.refs.time_filter).dropdown('set selected', '')
            $(self.refs.sort_filter).dropdown('set selected', '')
            if (!self.disallow_producer_selection) {
                $(self.refs.producer_filter).dropdown('set selected', '')
            }

            self.search()
        }

        self.search = function (query) {
            var filters = {q: query || self.refs.search.value}

            filters.start_date = self.refs.start_date.value || ''
            filters.end_date = self.refs.end_date.value || ''
            filters.date_flags = $(self.refs.time_filter).dropdown('get value')
            filters.sorting = $(self.refs.sort_filter).dropdown('get value')

            // We may not have a producer so grab preset one from page load if so
            filters.producer = $(self.refs.producer_filter).dropdown('get value')

            // If our filters are the same as before, just return
            if (JSON.stringify(self.old_filters) === JSON.stringify(filters)) {
                return
            }

            self.old_filters = filters
            self.loading = true
            self.update()

            CHAHUB.api.search(filters)
                .done(function (data) {
                    self.update({
                        loading: false,
                        results: data.results,
                        suggestions: data.suggestions,
                        showing_default_results: data.showing_default_results
                    })
                })
        }

        self.set_display_mode = function (mode) {
            self.display_mode = mode
            self.update()
        }
    </script>

    <style type="text/stylus">
        #particle_header
            // This is for the particles js animations to fit to this
            position relative
            margin-bottom 0

            canvas
                position absolute
                top 0
                right 0
                left 0
                bottom 0
                z-index -1
                background rgba(19, 48, 70, 0.9)

        #mobile-grid
            margin-top 0

        #searchbar
            width 100%
            margin-top 10px

            input
                background-color rgba(255, 255, 255, .95)

        #brand_logo
            position absolute
            width 180 * 1.618% px
            height 60 * 1.618% px
            opacity .85
            left 0
            top -2%
            cursor pointer
            filter brightness(0) invert(1)

            @media screen and (max-width 991px)
                display none

        #brand_logo_mobile
            filter brightness(0) invert(1)
            opacity .85
            position absolute
            width 42px
            height 42px
            margin-top 9px
            left 4%
            cursor pointer

            @media screen and (min-width 992px)
                display none

        #mobile-friendly-button
            max-height 30.84px
            width 100%
            @media screen and (max-width 645px)
                display none

        #results_container
            min-height 375px

        #search_wrapper .results
            margin-top 1px

        search-results #searchbar .button
            color #e2e2e2
            background-color #C7402D !important
            opacity .85

        search-results #searchbar .button:hover
            color #e2e2e2
            background-color #C7402D !important
            opacity .98

        .ui.labeled.icon.button:hover > .icon, .ui.labeled.icon.buttons:hover > .button > .icon
            color #e2e2e2
            background-color #C7402D !important

            .icon
                color #C7402D

        #mobile-friendly-button.active > i.icon
            color #e2e2e2 !important
            background-color #C7402D !important
            .icon
                color #e2e2e2 !important

        #login-button
            position relative
            margin-left -20px
            margin-top 11px

        .ui.button
            margin-top 10px
            color #e2e2e2
            background-color rgba(255, 255, 255, .15)
            font-weight 100

        .ui.button:hover
            color #3f3f3f
            background-color rgba(255, 255, 255, .65)

        #down_caret
            color #e2e2e2
            background-color rgba(255, 255, 255, .15)
            font-weight 100
            width 100%
            height 2px
            margin-bottom -10px
            line-height 2px
            border-radius 0
            @media screen and (min-width 646px)
                display none

        #mobile_drop button:hover
            color #3f3f3f
            background-color rgba(255, 255, 255, .65)
            line-height 2px
            border-radius 0
            @media screen and (min-width 646px)
                display none

        #mobile_drop
            margin-bottom -13px
            margin-top -40px
            opacity 0.8
            display inline
            @media screen and (min-width 646px)
                display none
                height 0

        #ellipses
            position absolute
            right -30px

            .button
                height 38px
                width 23.5px
                color #e2e2e2 !important
                background-color rgba(255, 255, 255, .15) !important

            .button:hover
                color #3f3f3f !important
                background-color rgba(255, 255, 255, .65) !important

            .icon
                display inherit
                cursor pointer
                text-align left
                margin 0

            @media screen and (min-width 768px)
                display none

        .loading
            opacity .5

        .loader
            position absolute
            top 50px !important
            left 0
            bottom 0
            right 0
    </style>
</search-results>

<search-result class="item">
    <!--<div class="image">
        <!--<img src="https://semantic-ui.com/images/wireframe/image.png">
        <img src="{ logo }">
    </div>
    <div class="content">
        <a class="header">{ title }</a>
        <div class="meta">
            <span class="price">$1200</span>
            <span class="stay">1 Month</span>
        </div>
        <div class="description">
            <p>Blah blah lorem ipsum dolor sit amet, description about a competition.</p>
        </div>
        <div class="extra">
            <div class="ui right floated primary button">
                Participate
                <i class="right chevron icon"></i>
            </div>
        </div>
    </div>-->
</search-result>

<competition-tile onclick="{redirect_to_url}">
    <div class="ui tiny image" style="width: 40px;">
        <img src="{logo}" style="margin-left: 1em; max-width: 3em; max-height: 3em;" class="ui avatar image">
    </div>
    <div class="content">
        <div class="header">
            {title}
        </div>
        <div class="description">
            <p>{description}</p>
        </div>
        <div class="extra" style="margin-top: 0;">
            <span style="font-size: .8em; color: rgba(0,0,255, 0.6);">{url}</span>
            <span style="font-size: .8em;">
                {pretty_date(start)}
                <virtual if="{end}">
                    - {pretty_date(end)}
                </virtual>
            </span>
            <div class="ui right floated blue mini label tooltip" data-content="Participant count">
                <i class="user icon"></i> {participant_count}
            </div>
            <div class="ui right floated mini label tooltip" data-content="Prize Amount" show="{prize}">
                <i class="yellow trophy icon"></i> {prize}
            </div>
            <div class="ui right floated red mini label tooltip"
                 style="background-color: #db28289e;"
                 data-content="Deadline of the current phase"
                 show="{current_phase_deadline}">
                <i class="alarm icon"></i> {pretty_date(current_phase_deadline)}
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
        })

        self.redirect_to_url = function () {
            window.open(self.url, '_blank');
        }
    </script>

    <style type="text/stylus">
        :scope
            display block

        .content
            .description
                margin-top 0 !important
                color #808080 !important
                font-size .9em !important

            p
                line-height 1.1em !important
    </style>
</competition-tile>

<competition-card>
    <div class="image">
        <img src="https://i.imgur.com/n2XUSxU.png">
    </div>
    <div class="content">
        <a class="header">{ title }</a>
        <div class="meta">
            <span class="date">Joined in 2013</span>
        </div>
        <div class="description">
            Kristy is an art director living in New York.
        </div>
    </div>
    <div class="extra content">
        <a>
            <i class="user icon"></i>
            22 Friends
        </a>
    </div>

    <script>
    </script>

    <style type="text/stylus">
        :self
            display block
    </style>
</competition-card>

<competition-mobile-tile onclick="{redirect_to_url}">
    <!--<h6 class="ui top attached header">
        Dogs
    </h6>
    <div class="ui grid attached segment">
        <div class="ui floating blue centered mini label tooltip" data-content="Participant count">
            <p style="">{participant_count}</p>
        </div>
        <div class="ui tiny image" style="width: 40px;">
            <img src="{logo}" style="margin-left: 1em; max-width: 3em; max-height: 3em;" class="ui avatar image">
        </div>
        <div class="content">
            <div class="header">
                {title}
            </div>
            <div class="description">
                <p>{description}</p>
            </div>
            <div class="extra" style="margin-top: 0;">
                <span style="font-size: .8em; color: rgba(0,0,255, 0.6);">{url}</span>
                <span style="font-size: .8em;">
                {pretty_date(start)}
                <virtual if="{end}">
                    - {pretty_date(end)}
                </virtual>
            </span>
                <div class="ui right floated mini label tooltip" data-content="Prize Amount" show="{prize}">
                    <i class="yellow trophy icon"></i> {prize}
                </div>
                <div class="ui right floated red mini label tooltip"
                     style="background-color: #db28289e;"
                     data-content="Deadline of the current phase"
                     show="{current_phase_deadline}">
                    <i class="alarm icon"></i> {pretty_date(current_phase_deadline)}
                </div>
            </div>
        </div>
    </div>-->
    <div class="ui attached message">
        <div class="ui grid">
            <div class="row">
                <div class="ui two wide centered column" style="text-align: center;">
                    <img src="{logo}" style="margin: 0em; max-width: 3em; max-height: 3em;"
                         class="ui centered avatar image">
                </div>
                <div class="fourteen wide column">
                    <div style="font-size: .95em;" class="header">
                        {title}
                    </div>
                    <p style="font-size: .85em; color: rgba(0,0,0, 0.4);">{description}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="ui attached fluid segment">
        <div class="ui floating blue centered mini label tooltip" data-content="Participant count">
            <p style="">{participant_count}</p>
        </div>
        <div align="center" class="">
            <div class="" style="margin-top: 0;">
                <span style="font-size: .8em; color: rgba(0,0,255, 0.6);">{url}</span>
            </div>
            <div>
                <span style="font-size: .8em;">
                    {pretty_date(start)}
                    <virtual if="{end}">
                        - {pretty_date(end)}
                    </virtual>
                </span>
            </div>
            <div class="ui right floated mini label tooltip" data-content="Prize Amount" show="{prize}">
                <i class="yellow trophy icon"></i> {prize}
            </div>
            <div class="ui right floated red mini label tooltip"
                 style="background-color: #db28289e;"
                 data-content="Deadline of the current phase"
                 show="{current_phase_deadline}">
                <i class="alarm icon"></i> {pretty_date(current_phase_deadline)}
            </div>
        </div>
    </div>
    </div>

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
        })

        self.redirect_to_url = function () {
            window.open(self.url, '_blank');
        }
    </script>

    <style type="text/stylus">
        :scope
            display block

        .content
            .description
                margin-top 0 !important
                color #808080 !important
                font-size .9em !important

            p
                line-height 1.1em !important
    </style>
</competition-mobile-tile>
