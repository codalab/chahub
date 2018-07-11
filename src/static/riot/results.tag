<search-results>
    <div id="particle_header" class="ui stackable centered grid top">
        <div class="ui row">
            <div class="one wide tablet four wide computer column">
                <!--<img class="ui image desktop-only" id="brand_logo" src="static/img/temp_chahub_logo.png">-->
                <img class="ui image" id="brand_logo_mobile" src="static/img/temp_chahub_logo.png">
            </div>
            <div class="two wide tablet eight wide computer column">
                <div class="ui double stackable centered grid">
                    <div class="centered row">
                        <div class="search-wrapper column">
                            <div class="ui left action right icon input">
                                <button class="ui red icon button" onclick="{ clear_search }">
                                    <i class="delete icon"></i>
                                </button>
                                <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">
                                <i class="search icon"></i>
                            </div>
                        </div>
                    </div>
                    <div class="centered row">
                        <div class="one wide tablet four wide computer center aligned column">
                            <div ref="time_filter" class="ui tiny labeled icon dropdown button">
                                <i class="calendar icon"></i>
                                <span class="text">Any time</span>
                                <div class="menu">
                                    <div class="header">
                                        Timeframe
                                    </div>
                                    <div class="divider"></div>
                                    <div class="active item" data-value="">
                                        Any time
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

                        <div class="one wide tablet four wide computer center aligned column">
                            <div ref="sort_filter" class="ui tiny labeled icon dropdown button">
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

                        <div class="one wide tablet four wide computer center aligned column"
                             show="{!disallow_producer_selection}">
                            <div ref="producer_filter" class="ui tiny labeled icon dropdown button">
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
            <div class="one wide tablet four wide computer center aligned column">
                <a hide="{USER_AUTHENTICATED}" style="" href="/accounts/login/"
                   class="ui red button">LOGIN</a>
                <a show="{USER_AUTHENTICATED}" style="" href="/accounts/logout/"
                   class="ui red button">LOGOUT</a>
            </div>
        </div>
    </div>
    <div class="ui centered grid">
        <div class="fourteen wide tablet eight wide computer column">
            <div class="ui stacked">
                <div class="ui warning message" show="{showing_default_results}">
                    <div class="header">
                        No results found
                    </div>
                    Try broadening your search
                </div>
                <div class="ui middle aligned compact divided link items" style="margin-top: 0;">
                    <competition-tile each="{ results }" no-reorder class="item"
                                      style="padding: .5em 0;"></competition-tile>
                </div>
            </div>
        </div>
    </div>

    <script>
        var self = this
        self.results = []
        self.display_mode = 'list'
        self.old_filters = {}

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
                onChange: function(date, text, mode) {
                    self.set_time_dropdown_text()

                    self.search()
                }
            })
            $(".ui.dropdown").dropdown({
                onChange: function(){
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

        self.set_time_dropdown_text = function() {
            /*if(this.dataset.calendarType === 'start') {
                self.refs.start_date.value = text
            }

            if(this.dataset.calendarType === 'end') {
                self.refs.end_date.value = text
            }*/

            if (self.refs.start_date.value && self.refs.end_date.value){
                var temp_string = self.refs.start_date.value + ' through ' + self.refs.end_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
            else if (self.refs.start_date.value){
                var temp_string = 'Starting from ' +  self.refs.start_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
            else if (self.refs.end_date.value){
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
            if(params.date_flags) {
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

        self.clear_search = function() {
            self.refs.search.value = ''
            self.refs.start_date.value = ''
            self.refs.end_date.value = ''
            $(self.refs.time_filter).dropdown('set selected', '')
            $(self.refs.sort_filter).dropdown('set selected', '')
            if (!self.disallow_producer_selection){
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
            if(JSON.stringify(self.old_filters) === JSON.stringify(filters)) {
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

        .content-desktop {
            display: block;
        }

        .content-mobile {
            display: none;
        }

        @media screen and (max-width: 768px) {

            .content-desktop {
                display: none;
            }

            .content-mobile {
                display: block;
            }

        }

        /*
        //medium+ screen sizes
        @media (min-width: 992px) {
            .desktop-only {
                display: block !important;
            }
        }

        //small screen sizes
        @media (max-width: 991px) {
            .mobile-only {
                display: block !important;
            }

            .desktop-only {
                display: none !important;
            }
        }*/

        .ui.grid
            @media screen and (max-width: 640px)
                margin 0rem !important

        .ui.top
            // This is for the particles js animations to fit to this
            position relative

            canvas
                position absolute
                top 0
                right 0
                left 0
                bottom 0
                z-index -1
                background rgba(22, 12, 160, 0.9)

        #brand_logo
            height 48px
            position absolute
            top 10px
            cursor pointer
            filter brightness(0) invert(1)

        #brand_logo_mobile
            filter brightness(0) invert(1)

        #results_container
            min-height 375px

        #search_wrapper .results
            margin-top 1px

        .ui.button:hover .icon
            opacity 1

        .search-wrapper
            padding-bottom 0 !important

            .input
                width 100% !important
            @media screen and (max-width: 640px)
                .input
                    width 40%

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
