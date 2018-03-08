<search-results>
    <div id="particle_header" class="ui top">
        <div class="ui grid container menu-holder">
            <div class="centered column twelve wide">
                <div class="ui grid">
                    <div class="row search-wrapper">
                        <div class="ui left action right icon input">
                            <button class="ui red icon button" onclick="{ clear_search }">
                                <i class="delete icon"></i>
                            </button>
                            <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">
                            <i class="search icon"></i>
                        </div>
                    </div>
                    <div class="row">
                        <div class="ui form">
                            <div class="inline fields">
                                <div class="field">
                                    <div ref="time_filter" class="ui floating labeled icon dropdown button">
                                        <i class="calendar icon"></i>
                                        <span class="text">Any time</span>
                                        <div class="menu">
                                            <div class="header">
                                                Timeframe
                                            </div>
                                            <div class="divider"></div>
                                            <div class="active item" data-value="any_time">
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

                                <div class="field">
                                    <div ref="sort_filter" class="ui floating labeled icon dropdown button">
                                        <i class="filter icon"></i>
                                        <span class="text">Sort by relevance</span>
                                        <div class="menu">
                                            <div class="item">
                                                Sort by relevance
                                            </div>
                                            <div data-value="deadline" class="item">
                                                Next deadline
                                            </div>
                                            <div data-value="prize" class="item">
                                                Prize amount
                                            </div>
                                            <div data-value="participant_count" class="item">
                                                Number of participants
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!--<div class="field">
                                    <div class="ui icon buttons">
                                        <button class="ui button { positive: display_mode === 'list' }"
                                                onclick="{ set_display_mode.bind(this, 'list') }">
                                            <i class="list layout icon"></i>
                                        </button>
                                        <button class="ui button { positive: display_mode === 'card' }"
                                                onclick="{ set_display_mode.bind(this, 'card') }">
                                            <i class="grid layout icon"></i>
                                        </button>
                                    </div>
                                </div>-->
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <!--<div class="item column three wide">
                <div class="ui input">
                    <!--<div class="ui inverted blue button">Create Competition</div>
                </div>
            </div>-->
        </div>
        <!--<div class="item">
            <div class="ui icon input">
                <input type="text" placeholder="Search...">
                <i class="search icon"></i>
            </div>
        </div>
        <div class="right item">
            <div class="ui input">
                <div class="ui primary button">Create Competition</div>
            </div>
        </div>-->
    </div>

    <div class="ui stackable grid container">
        <div class="row centered">
            <div class="twelve wide column">
                <div class="ui active centered inline loader"
                     show="{loading}"
                     style="margin: 20px auto;"></div>
            </div>
        </div>
        <div id="results_container" class="row centered">
            <div class="twelve wide column" style="padding: 0;" show="{ display_mode === 'list' }">
                <div class="ui stacked">
                    <!--<div class="ui message" show="{!showing_default_results}">
                        <div class="header">
                            {results.length}
                        </div>
                        Results
                    </div>-->
                    <div class="ui warning message" show="{showing_default_results}">
                        <div class="header">
                            No results found
                        </div>
                        Try broadening your search
                    </div>

                    <div class="ui middle aligned compact divided link items" style="margin-top: 0;">
                        <competition-tile each="{ results }" no-reorder class="item" style="padding: .5em 0;"></competition-tile>
                    </div>

                    <!--<div class="ui link cards">
                        <competition-card each="{ results }" class="ui centered card"
                                          show="{ display_mode === 'card' }"></competition-card>
                    </div>-->
                </div>
            </div>
            <div class="sixteen wide column" show="{ display_mode === 'card' }">
                <div class="ui stacked">
                    <!--<search-result each="{ results }"></search-result>-->
                    <div id="result_header" style="background-color: #efefef; padding: 10px; margin-bottom: 20px;">
                        <h3 class="ui inverted">{ results.length } results</h3>
                    </div>
                    <div class="ui link cards">
                        <competition-card each="{ results }" class="ui centered card"></competition-card>
                    </div>
                    <div show="{ results.length == 0 }">
                        <i>No results found...</i>
                    </div>
                </div>
            </div>
        </div>

        <!--<div class="row centered">
            <div class="twelve wide column right aligned">
                <div class="ui pagination menu right aligned">
                    <a class="active item">
                        1
                    </a>
                    <div class="disabled item">
                        ...
                    </div>
                    <a class="item">
                        10
                    </a>
                    <a class="item">
                        11
                    </a>
                    <a class="item">
                        12
                    </a>
                </div>
            </div>
        </div>-->
    </div>

    <script>
        var self = this
        self.results = []
        self.display_mode = 'list'
        self.start_date = null
        self.end_date = null
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
                    if(this.dataset.calendarType === 'start') {
                        self.start_date = text
                    }

                    if(this.dataset.calendarType === 'end') {
                        self.end_date = text
                    }

                    if (self.start_date && self.end_date){
                        var temp_string = self.start_date + ' through ' + self.end_date
                        $(self.refs.time_filter).dropdown('set text', temp_string)
                    }
                    else if (self.start_date){
                        var temp_string = 'Starting From: ' +  self.start_date
                        $(self.refs.time_filter).dropdown('set text', temp_string)
                    }
                    else if (self.end_date){
                        var temp_string = 'End By: ' + self.end_date
                        $(self.refs.time_filter).dropdown('set text', temp_string)
                    }

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


        self.on('route', function () {
            var params = route.query()

            // On page load set search bar to search and execute search if we were given a query
            self.refs.search.value = params.q || ''
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
            self.start_date = ''
            self.end_date = ''
            self.refs.start_date.value = ''
            self.refs.end_date.value = ''
            $(self.refs.time_filter).dropdown('set text', 'Any time')
            $(self.refs.time_filter).dropdown('restore defaults');
            $(self.refs.sort_filter).dropdown('set text', 'Sort by relevance')
            $(self.refs.sort_filter).dropdown('restore defaults');


            // TODO: CLEAR DATES AND SUCH ???

            self.search()
        }

        self.search = function (query) {
            var filters = {q: query || self.refs.search.value}

            if (self.refs.start_date.value) {
                filters.start_date = self.refs.start_date.value
            }
            if (self.refs.end_date.value) {
                filters.end_date = self.refs.end_date.value
            }

            filters.date_flags = $(self.refs.time_filter).dropdown('get value')
            filters.sorting = $(self.refs.sort_filter).dropdown('get value')

            if(JSON.stringify(self.old_filters) === JSON.stringify(filters)) {
                return
            } else {
                self.old_filters = filters
            }
            
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

        #results_container
            min-height 375px

        #search_wrapper .results
            margin-top 1px

        .ui.button:hover .icon
            opacity 1

        .search-wrapper
            padding-bottom 0 !important

            .input
                width 100%
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
        <img src="{logo}" style="margin-left: 1em; width: 3em; height: 3em;" class="ui avatar image">
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
            <div class="ui right floated red mini label tooltip"
                 style="background-color: #db28289e;"
                 data-content="Deadline of the current phase"
                 show="{current_phase_deadline}">
                <i class="alarm icon"></i> {pretty_date(current_phase_deadline)}
            </div>
        </div>
    </div>


    <!--<div class="ui grid">
        <div class="ui row">
            <div align="center" class="one wide column">
                <img class="ui avatar image" src="{logo}">
            </div>
            <div class="eight wide left aligned column">
                <div class="header">{title}</div>
                <i class="comp-description">{description}</i>
                <br>
                <i style="font-size: 12px !important;">
                    {pretty_date(start_date)}
                    <virtual if="{end}">
                        - {pretty_date(end)}
                    </virtual>
                </i>
            </div>
            <div class="two wide column">
                <!--<i>{created_by}</i>
            </div>
            <div class="three wide middle aligned column">
                <i style="font-size: 10px !important;">{pretty_date(phase_deadlines)}</i>
            </div>
            <div class="two wide column">
                <div class="ui blue label">
                    <i class="user icon"></i> {participant_count}
                </div>
            </div>
        </div>
    </div>-->

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()

            /*if (self.description) {
                if (self.description.length > 75){
                    self.description = self.description.substr(0, 75) + "..."
                    self.update()
                }
            }*/
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
