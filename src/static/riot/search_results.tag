<search-results>
    <competition-modal></competition-modal>
    <div id="particle_header" class="ui centered grid">
        <span hide="{ embedded }">
            <user-button></user-button>
        </span>

        <div id="top_row" class="ui row">
            <img id="brand_logo" src="static/img/temp_chahub_logo_beta.png">
            <img id="brand_logo_mobile" src="static/img/Chahub_C.png">

            <!-- We keep 1 empty column here to align the brand logo defined above this element -->
            <div class="one wide column"></div>

            <div class="eleven wide mobile twelve wide tablet nine wide computer ultrawide column">
                <div class="ui centered grid">
                    <div class="ui centered row">
                        <div class="ui sixteen wide mobile fifteen wide search-wrapper column">
                            <div id="searchbar" class="ui left action input">
                                <button class="ui icon button" onclick="{ clear_search }">
                                    <i class="delete icon"></i>
                                </button>
                                <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">

                                <div id="search-filter" class="ui multiple dropdown icon button" ref="object_types">
                                    <i class="filter icon"></i>
                                    <span class="text"></span>
                                    <div class="menu">
                                        <div class="item" data-value="all">
                                            <i class="globe icon"></i>
                                            <span class="label-text">All</span>
                                        </div>
                                        <!--<div class="item" data-value="user">
                                            <i class="users icon"></i>
                                            <span class="label-text">Users</span>
                                        </div>
                                        <div class="item" data-value="profile">
                                            <i class="users icon"></i>
                                            <span class="label-text">Profiles</span>
                                        </div>-->
                                        <div class="item" data-value="data">
                                            <i class="file icon"></i>
                                            <span class="label-text">Datasets</span>
                                        </div>
                                        <div class="item" data-value="competitions">
                                            <i class="server icon"></i>
                                            <span class="label-text">Competitions</span>
                                        </div>
                                        <!--<div class="item" data-value="tasks">
                                            <i class="hdd icon"></i>
                                            <span class="label-text">Tasks</span>
                                        </div>
                                        <div class="item" data-value="solutions">
                                            <i class="code icon"></i>
                                            <span class="label-text">Solutions</span>
                                        </div>-->
                                    </div>
                                </div>
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
                    <i class="sort icon"></i>
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
                        <virtual each="{CHAHUB.state.producers}">
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
                <!--<div class="ui success message" show="{ results.length > 0 && !showing_default_results }">
                    Found { results.length } results
                </div>-->
                <div class="ui middle aligned unstackable compact divided link items content-desktop">
                    <virtual each="{result in results}">
                        <competition-tile if="{result.index_type === 'competitions'}" comp="{result}" no-reorder class="item"></competition-tile>
                        <dataset-tile if="{result.index_type === 'data'}" dataset="{result}" no-reorder class="item"></dataset-tile>
                    </virtual>

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

        self.on('mount', function () {
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
            $(self.refs.object_types).dropdown('set selected', params.index)

            // Dropdown actions (listen AFTER we set dropdowns, so double search doesn't happen!)
            $(".dropdown", self.root).dropdown({
                onChange: function (text, value) {
                    self.search()
                }
            })

            // For iframes we might want to hide producer selection
            self.embedded = params.embedded

            if (CHAHUB.state.default_search_results && _.isEmpty(params)) {
                console.log("Loading default search results")
                self.results = CHAHUB.state.default_search_results
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
            let index = $(self.refs.object_types).dropdown('get value')
            filters.index = index && index !== 'all' ? index : null
            if (index && index !== 'all') {
                filters.index = index
            }
            // Remove any unused filters so we don't do empty searches
            filters = _.omitBy(filters, _.isEmpty)

            // If we don't need to search.. don't! either it's the same search or empty
            if (JSON.stringify(self.old_filters) === JSON.stringify(filters)) {
                return
            }

            self.old_filters = filters
            self.loading = true
            self.update()

            CHAHUB.api.search(filters)
                .done(function (data) {
                    console.log(data.results)
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

        .search-wrapper
            z-index 2

        #search-filter
            margin-left 10px
            border-radius 4px
            padding 0.5em 0.25em 0.5em 0.75em

            > .label
                margin 0 .14285714em

                .label-text
                    display none

                > .icon
                    margin 0 .25rem 0 0
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
