<search-results>
    <competition-modal></competition-modal>
    <div id="particle_header" class="ui centered grid">
        <span hide="{ embedded }">
            <a id="login-button" hide="{USER_AUTHENTICATED}" href="/accounts/login/"
               class="ui button">LOGIN
            </a>
            <a id="login-button" show="{USER_AUTHENTICATED}" href="/accounts/logout/"
               class="ui button">LOGOUT
            </a>
        </span>

        <!--<div id="hamburger_button">
            <div class="ui small icon button">
                <i class="large bars icon"></i>
            </div>
        </div>-->

        <div id="top_row" class="ui row">
            <img id="brand_logo" src="static/img/temp_chahub_logo_beta.png">
            <img id="brand_logo_mobile" src="static/img/Chahub_C.png">

            <!-- We keep 1 empty column here to align the brand logo defined above this element -->
            <div class="one wide column"></div>

            <div class="eleven wide mobile twelve wide tablet nine wide computer ultrawide column">
                <div class="ui centered grid">
                    <div class="ui centered row">
                        <div class="ui sixteen wide mobile fifteen wide search-wrapper column">
                            <div id="searchbar" class="ui left action right icon input">
                                <button class="ui icon button" onclick="{ clear_search }">
                                    <i class="delete icon"></i>
                                </button>
                                <input type="text" placeholder="Search..." ref="search"
                                       onkeydown="{ input_updated }">
                                <i class="search icon"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet computer only one wide column">
            </div>
        </div>
        <!-- Buttons below searchbar on particle header. Only seen above 646px wide screens. -->
        <!-- This column is removed for mobile to align with top row -->
        <div id="remove_mobile" class="ui one wide column"></div>
        <div id="advanced_search_column"
             class="ui ultrawide centered eleven wide mobile twelve wide tablet nine wide computer {hide-from-mobile: !display_search_options} column">
            <div id="advanced_search_align" class="five wide center aligned column">
                <div id="advanced_search_button" ref="time_filter"
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
                                   placeholder=" Start date">
                        </div>
                        <div class="ui left icon input datepicker" data-calendar-type="end">
                            <i class="calendar icon"></i>
                            <input ref="end_date" type="text" name="search" placeholder=" End date">
                        </div>
                    </div>
                </div>
            </div>
            <div id="advanced_search_align" class="middle six wide center aligned column">
                <div id="advanced_search_button" ref="sort_filter"
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
            <div id="advanced_search_align" class="five wide center aligned column"
                 show="{!embedded}">
                <div id="advanced_search_button" ref="producer_filter"
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
        <div class="advanced search ui row">
            <div id="mobile_drop" class="sixteen wide mobile only column">
                <button id="down_caret" class="ui icon button" onclick="{ toggle_search_options }">
                    <i class="{up: display_search_options}{down: !display_search_options} caret icon"></i>
                    Advanced Search
                </button>
            </div>
        </div>
    </div>
    <div id="mobile-grid" class="ui centered grid { fix-left: !show_stats }">
        <div id="mobile" class="sixteen wide tablet twelve wide computer column">
            <div class="ui stacked">
                <div class="ui warning message" show="{ results.length === 0 && !showing_default_results && !loading }">
                    <div class="header">
                        No results found
                    </div>
                    Try broadening your search
                </div>
                <div class="ui success message" show="{ results.length > 0 && !showing_default_results }">
                    Found { results.length } results
                </div>
                <div class="ui middle aligned unstackable compact divided link items content-desktop">
                    <competition-tile each="{ results }" no-reorder class="item"></competition-tile>
                </div>
                <!--<div class="ui middle aligned compact link items content-mobile" style="margin-top: -1;">
                    <competition-mobile-tile each="{ results }" no-reorder class="item"
                                             style="padding: -1em;"></competition-mobile-tile>
                </div> -->
            </div>
        </div>
        <div class="four wide right floated computer only column">
            <show-stats></show-stats>
        </div>
    </div>

    <script>
        var self = this
        self.results = []
        self.display_mode = 'list'
        self.loading = true
        self.old_filters = {}
        self.display_search_options = false

        self.one('mount', function () {
            // header particles
            particlesJS.load('particle_header', URLS.assets.header_particles)

            // Datepickers
            $('.datepicker').calendar({
                type: 'date',
                formatter: {
                    date: function (date, settings) {
                        return luxon.DateTime.fromJSDate(date).toISODate()
                    }
                },
                startCalendar: ".datepicker[data-calendar-type='start']",
                endCalendar: ".datepicker[data-calendar-type='end']",
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

            // Sidebar with overlay on
            //$('.sidebar')
            //    .sidebar({
            //        transition: 'overlay',
            //    })
            //    .sidebar('attach events', '#hamburger_button');

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
            })

            /*// Loading the search results
            if (DEFAULT_SEARCH_RESULTS) {
                self.results = DEFAULT_SEARCH_RESULTS
                self.update()
            } else {
                self.search()
            }

            // Focus on search
            self.refs.search.focus()*/

            self.init_values_from_query_params()
        })

        self.toggle_search_options = function () {
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
            } else if (self.refs.start_date.value) {
                var temp_string = 'Starting from ' + self.refs.start_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            } else if (self.refs.end_date.value) {
                var temp_string = 'End by ' + self.refs.end_date.value
                $(self.refs.time_filter).dropdown('set text', temp_string)
            }
        }


        self.init_values_from_query_params = function () {
            var params = route.query()

            // On page load set search bar to search and execute search if we were given a query
            // Decoding the URI query for the search bar, must decodeURI after the or statement or
            // returns undefined in search params
            self.refs.search.value = params.q || ''
            self.refs.search.value = decodeURI(self.refs.search.value)

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

            // Dropdowns
            $(self.refs.sort_filter).dropdown('set selected', params.sorting)
            $(self.refs.producer_filter).dropdown('set selected', params.producer)

            // Dropdown actions (listen AFTER we set dropdowns, so double search doesn't happen!)
            $(".dropdown", self.root).dropdown({
                onChange: function (text, value) {
                    self.search()
                }
            })

            // For iframes we might want to hide producer selection
            self.embedded = params.embedded

            if (DEFAULT_SEARCH_RESULTS && $.isEmptyObject(params)) {
                console.log("Loading default search results")
                self.results = DEFAULT_SEARCH_RESULTS
                self.showing_default_results = true
                self.prepare_results()
                self.update()
            } else {
                // We have some search to perform, not just displaying default results
                self.search()
            }

            // Focus on search
            self.refs.search.focus()
        }

        self.input_updated = function () {
            delay(function () {
                self.search()
            }, 250)
        }

        self.prepare_results = function () {
            self.results.forEach(function (comp_result) {
                var humanized_time = humanize_time(comp_result.current_phase_deadline)
                comp_result.alert_icon = humanized_time < 0;
                if (comp_result.alert_icon) {
                    comp_result.pretty_deadline_time = 'Phase ended ' + Math.abs(humanized_time) + ' days ago'
                } else {
                    comp_result.pretty_deadline_time = humanized_time
                }
            })
        }

        self.clear_search = function () {
            self.refs.search.value = ''
            self.refs.start_date.value = ''
            self.refs.end_date.value = ''
            $(self.refs.time_filter).dropdown('set selected', '')
            $(self.refs.sort_filter).dropdown('set selected', '')
            if (!self.embedded) {
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

            // Remove any unused filters so we don't do empty searches
            dict_remove_empty_values(filters)

            // If we don't need to search.. don't! either it's the same search or empty
            if (JSON.stringify(self.old_filters) === JSON.stringify(filters)) {
                return
            }

            console.log("Doing search with filters:")
            console.log(filters)
            console.trace()

            self.old_filters = filters
            self.loading = true
            self.update()

            CHAHUB.api.search(filters)
                .done(function (data) {
                    self.loading = false
                    self.suggestions = data.suggestions
                    self.showing_default_results = data.showing_default_results
                    self.results = data.results
                    self.prepare_results()
                    self.update()
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

        .advanced.search.ui.row
            padding 0 0

        #mobile-grid
            margin-top 0

        .fix-left
            margin-left 50px !important

        #remove_mobile
            @media screen and (max-width 645px)
                display none
            @media screen and (min-width 768px)
                display none

        #searchbar
            width 100%
            margin-top 10px

            input
                background-color rgba(255, 255, 255, .95)
                padding-right 0 !important

            // stylus was messing up auto-formatting on media queries so I used standard CSS
            @media screen and (max-width 500px) {
                margin-left: -1em;
            }
            @media screen and (max-width 400px) {
                margin-left: -1em;
            }
            @media screen and (max-width 350px) {
                left: -24px;
            }
            @media screen and (min-width 2560px) {
                font-size: 1.4rem;
            }

        #brand_logo
            position absolute
            width 180 * 1.618% px
            opacity .85
            left 0
            top -2%
            cursor pointer
            filter brightness(0) invert(1)

            @media screen and (max-width 1100px)
                display none

            @media screen and (min-width 2560px)
                top 50%
                left 50px

        #brand_logo_mobile
            filter brightness(0) invert(1)
            opacity .85
            position absolute
            width 42px
            height 42px
            margin-top 9px
            left 4%
            cursor pointer

            @media screen and (min-width 1101px)
                display none
            @media screen and (max-width 350px)
                display none

        #advanced_search_column
            display flex
            text-align center
            padding-top 0
            padding-bottom 0
            margin 0 1.5em 0 1.5em

            @media screen and (min-width 646px)
                padding-bottom 10px
            @media screen and (max-width 645px)
                width 100% !important

        #advanced_search_align
            display flex
            justify-content center
            width 100%

        .middle
            margin-right 10px !important
            margin-left 10px !important
            @media screen and (max-width 334px)
                margin-right 3px !important
                margin-left 3px !important

        #advanced_search_button
            width 100%
            min-width 120px
            display flex
            justify-content center
            flex-direction column
            text-align center
            margin-right 0

            @media screen and (max-width 390px)
                min-width 100px
                padding-left 2.8em !important;

            @media screen and (min-width 2560px)
                font-size 1.4rem

        .ui.dropdown .menu > .item
            @media screen and (min-width 2560px)
                font-size 1.4rem

        .hide-from-mobile
            //display none !important
            @media screen and (max-width 645px)
                display none !important

        #top_row
            padding-bottom 0

        #search-flex
            display flex
            text-align center
            margin-top 10px
            padding-right 10px
            padding-left 10px

        #search-options-column
            width 100%
            padding 1em 0
            display flex
            justify-content center

        #search-options-button
            color #5e5e5f
            border solid 1px rgba(40, 40, 40, .15)
            justify-content center
            width: 95%
            margin -1em 0 0 0
            background-color rgb(244, 245, 246)
            text-align center
            display flex
            flex-direction column

            .icon
                background-color #C7402D
                color #e2e2e2
                border-top-left-radius 3px
                border-bottom-left-radius 3px
            @media screen and (min-width 646px)
                display none

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

        #advanced_search_button.active > i.icon
            color #e2e2e2 !important
            background-color #C7402D !important

            .icon
                color #e2e2e2 !important

        #login-button
            position absolute
            right 20px
            top 15px
            z-index 1000
            @media screen and (max-width 767px)
                display none
            @media screen and (min-width 2560px)
                font-size 1.4rem

        .ui.button
            margin-top 10px
            color #e2e2e2
            background-color rgba(255, 255, 255, .15)
            font-weight 100

        .ui.button:hover
            color #3f3f3f

            .icon
                opacity 1 !important

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
            bottom 0
            padding-right 0
            opacity 0.8
            display inline
            z-index 10
            width 100vw
            @media screen and (min-width 646px)
                display none
                height 0

        #hamburger_button
            position absolute
            top 25px
            right 10px
            z-index 1000

            .button
                color #e2e2e2 !important
                background-color rgba(255, 255, 255, .15) !important
                height 36px

            .button:hover
                color #3f3f3f !important
                background-color rgba(255, 255, 255, .65) !important

            .icon
                display inherit
                cursor pointer
                margin 0
                height 36px

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

        #calendarstyling
            background-color white !important
            opacity 1 !important
            z-index 1000
            // Buttons on calendar

            .icon
                background-color transparent
                border none

            // Buttons on Date Range Input

            .calendar.icon
                background-color #e2e2e2
                color #6f6f6f
                border solid #e2e2e2 1px
                border-left none
                border-right solid #e2e2e2 1px

        competition-tile
            padding-bottom 0 !important

        h4.sub.header,
        .ui.statistic > .label, .ui.statistics .statistic > .label,
        .ui.statistic > .value, .ui.statistics .statistic > .value
            color #808080 !important

        .content-desktop
            margin 15px auto !important
            max-width 1350px

            @media screen and (min-width 2560px)
                margin 30px auto !important
                max-width 1750px
    </style>
</search-results>

<search-result class="item">
    <!--<div class="image">
        <img src="https://semantic-ui.com/images/wireframe/image.png">
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
    <div class="floating-actions { is-admin: USER_IS_SUPERUSER }">
        <i class="icon green pencil alternate"
           onclick="{ edit_competition }"></i>
        <i class="icon red delete" onclick="{ delete_competition }"></i>
        <i class="icon { yellow: locked, unlock: locked, lock: !locked }" onclick="{ lock_competition}"></i>
    </div>
    <div class="ui tiny image">
        <img src="{logo || URLS.STATIC('img/img-wireframe.png')}" class="ui avatar image">
    </div>
    <div class="content">
        <div class="header">
            {title}
        </div>
        <div class="description">
            <p>{description}</p>
        </div>
        <div class="extra">
            <div class="mobile_linewrap">
                <span class="url"><a href="{url}">{url_short(url)}</a></span>
                <span class="date">
                {pretty_date(start)}
                <virtual if="{end}">
                    - {pretty_date(end)}
                </virtual>
            </span>
                <div class="mobile_labelwrap"></div>
                <span class="participant_label ui right floated mini label tooltip" data-content="Participant count">
                    <i class="user icon"></i> {participant_count}
                </span>
                <span class="deadline_label ui right floated mini label tooltip {red: !alert_icon}"
                      data-content="Deadline of the current phase"
                      show="{current_phase_deadline}">
                    <i show="{!alert_icon}" class="alarm icon"></i> {pretty_deadline_time}
                </span>
                <span class="deadline_label ui right floated mini label" show="{!current_phase_deadline}">
                    Never ends
                </span>
                <span class="prize_label ui right floated mini label tooltip" data-content="Prize Amount"
                      show="{prize}">
                    <i class="yellow trophy icon"></i> {prize}
                </span>
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
            $(self.refs.modal).modal()
        })

        self.redirect_to_url = function () {
            window.open(self.url, '_blank');
        }

        self.url_short = function (url) {
            return url.replace(/^(?:https?:\/\/)?(?:www\.)?/i, "").split('/')[0];
        }

        self.edit_competition = function (event) {
            CHAHUB.events.trigger('competition_selected', event.item)
            event.cancelBubble = true
        }

        self.delete_competition = function (event) {
            // TODO - Need to delete the competition on confirm, else do nothing.
            if (confirm(`Are you sure you want to delete "${event.item.title}?"`)) {
                alert('Deleted')
            }
            event.cancelBubble = true
        }

        self.lock_competition = function (event) {
            // TODO - Need to lock the competition and change icon/color to represent locked and unlocked state
            event.cancelBubble = true
        }
    </script>

    <style type="text/stylus">
        :scope
            display block
            position relative

        :scope:hover .floating-actions.is-admin
            opacity 1

        .floating-actions
            position absolute
            top 0
            right 0
            opacity 0
            z-index 10

        .content
            .description
                margin-top 0 !important
                color #808080 !important
                display block
                font-size .9em !important

            p
                line-height 1.1em !important

            @media screen and (max-width 645px)
                padding-left 0.8em !important

        .extra
            margin-top 0
            @media screen and (max-width 749px)
                margin-bottom 0 !important

            .url
                font-size .8em
                color rgba(0, 0, 255, 0.6) !important
                white-space nowrap
                overflow hidden
                text-overflow ellipsis
                max-width 90vw
                display block !important
                @media screen and (min-width 2560px)
                    margin-bottom: 10px;
                    overflow: visible;
                @media screen and (max-width 750px) {
                    margin-bottom: -6px;
                }

            .date
                font-size 0.8em
                color #8c8c8c !important

        .ui.avatar.image
            max-width 4em
            @media screen and (max-width 750px)
                max-width 3em
            @media screen and (min-width 2560px)
                max-width 8em

        .ui.image
            max-width 60px
            display inline-grid !important
            justify-content center
            @media screen and (min-width 2560px)
                max-width 240px

        .participant_label
            background-color #475e6f !important
            border-color #475e6f !important
            color #dfe3e5 !important
            right 0
            margin 0 2px !important
            text-align right

            .icon
                float left

        .prize_label
            background-color rgba(99, 84, 14, 0.68) !important
            border-color rgba(99, 84, 14, 0.68) !important
            color #dee2e4 !important
            margin 0 2px !important

        .deadline_label
            margin 0 2px !important

        .mobile_linewrap
            white-space nowrap
            overflow hidden
            text-overflow ellipsis
            color rgba(0, 0, 255, 0.6)
            margin-bottom 5px !important
            margin-right 0 !important

        .label
            @media screen and (min-width 2560px)
                font-size 1.2rem !important

        .mobile_labelwrap
            display block
            @media screen and (min-width 500px)
                display inline-block

        @media screen and (min-width 2560px)
            *
                font-size 1.5rem !important

            .header
                font-size 2rem !important

    </style>
</competition-tile>

<show-stats>
    <button id="stats-btn" onclick="{ stats_button_clicked }"
            class="ui black big launch left attached fixed button">
        <i class="icon {minus: !show_stats, 'chart bar': show_stats}"></i>
        <span class="btn-text">Stats</span>
    </button>
    <div id="stat-card" show="{ !show_stats }" class="ui card">
        <div class="content">
            <div class="header">By the numbers...</div>
        </div>
        <div class="content">
            <h4 class="ui sub blue header">Chahub brings together</h4>
            <div class="ui two column grid">
                    <div class="column" each="{ stat in producer_stats }" no-reorder>
            <div class="ui six tiny statistics">
                <div class="statistic">
                    <div class="value">
                        { stat.count }
                    </div>
                    <div class="label">
                        { stat.label }
                    </div>
                </div>
            </div>
                </div>
            </div>

        </div>
    </div>

    <script>
        var self = this
        self.show_stats = false
        self.producer_stats = {}

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
            self.get_general_stats()
        })

        self.get_general_stats = function () {
            CHAHUB.api.get_producer_stats()
                .done(function (data) {
                    console.log("Received general stats")
                    self.update({
                        producer_stats: [
                            {label: "Competitions", count: num_formatter(data.competition_count, 1)},
                            {label: "Datasets", count: num_formatter(data.dataset_count, 1)},
                            {label: "Participants", count: num_formatter(data.participant_count, 1)},
                            {label: "Submissions", count: num_formatter(data.submission_count, 1)},
                            {label: "Users", count: num_formatter(data.user_count, 1)},
                            {label: "Organizers", count: num_formatter(data.organizer_count, 1)},
                        ],
                    })
                })
        }

        self.stats_button_clicked = function () {
            self.show_stats = !self.show_stats
            self.update()
        }
    </script>

    <style type="text/stylus">
        #stats-btn
            position fixed
            top 110px
            right 0 !important
            width 55px
            height auto
            white-space nowrap
            overflow hidden
            transition 0.3s width ease, 0.5s transform ease

            .icon
                margin 0 .5em 0 -0.45em

        #stats-btn:hover
            width 130px

            .btn-text
                opacity 1

        .btn-text
            position absolute
            white-space nowrap
            top auto
            right 54px
            opacity 0
            -webkit-transition 0.23s opacity 0.2s
            -moz-transition 0.23s opacity 0.2s
            -o-transition 0.23s opacity 0.2s
            -ms-transition 0.23s opacity 0.2s
            transition 0.23s opacity 0.2s

        #stat-card
            z-index -1

        .ui.card>.content, .ui.cards>.card>.content
            padding-right 3em

        .ui.card>.content>.sub.header
            padding-bottom 10px

        .ui.statistics>.statistic
            flex 1 1 auto
    </style>
</show-stats>

<competition-modal>
    <div class="ui modal competition-form" ref="modal">
        <i class="close icon"></i>
        <div class="header">
            Edit Competition
        </div>
        <div style="padding: 20px;" class="edit-competition-form ui form">
            <div class="field">
                <label for="competition-title">Title</label>
                <input id="competition-title" type="text" class="ui input" ref="competition_title" name="title">
            </div>
            <div class="field">
                <label for="competition-description">Description</label>
                <textarea class="ui input" ref="competition_description" id="competition-description"
                          name="description"></textarea>
            </div>
            <div class="field">
                <label for="logo-url">Logo URL</label>
                <input type="url" class="ui input" ref="competition_logo" id="logo-url" name="logo">
            </div>
        </div>
        <div class="actions">
            <div class="ui black deny button">
                Cancel
            </div>
            <div class="ui positive right labeled icon button">
                Submit
                <i class="checkmark icon"></i>
            </div>
        </div>
    </div>

    <script>
        var self = this

        CHAHUB.events.on('competition_selected', function (competition) {
            self.selected_competition = competition
            self.refs.competition_title.value = self.selected_competition.title
            self.refs.competition_description.value = self.selected_competition.description
            self.refs.competition_logo.value = self.selected_competition.logo
            console.log(self)
            self.update()
            $(self.refs.modal).modal('show')
        })
    </script>
</competition-modal>

<competition-card>
    <!-- <div class="image">
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
    </style>-->
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
    </div>
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
        <div id="participant_label" class="ui floating centered mini label tooltip" data-content="Participant count">
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
            <div id="prize_label" class="ui right floated mini label tooltip" data-content="Prize Amount" show="{prize}">
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
