<search-results>
    <div id="particle_header" class="ui top">
        <div class="ui grid container menu-holder">
            <div class="item column thirteen wide">
                <div class="ui grid">
                    <div class="row search-wrapper">
                        <div class="ui icon input">
                            <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">
                            <i class="search icon"></i>
                        </div>
                    </div>
                    <div class="row">
                        <div class="ui form">
                            <div class="inline fields">
                                <div class="field">
                                    <div id="time-filters" class="ui floating labeled icon dropdown button" onkeydown="{ input_updated }">
                                        <i class="filter icon"></i>
                                        <span class="text">Any time</span>
                                        <div class="menu">
                                            <div class="header">
                                                Timeframe
                                            </div>
                                            <div class="divider"></div>
                                            <div class="item" data-value="active">
                                                Active
                                            </div>
                                            <div class="item" data-value="past_month">
                                                Started past month
                                            </div>
                                            <div class="item" data-value="past_year">
                                                Started past year
                                            </div>
                                            <div class="divider"></div>
                                            <div class="header">
                                                Date range
                                            </div>
                                            <div class="ui left icon input datepicker">
                                                <i class="calendar icon"></i>
                                                <input ref="start_date" type="text" name="search"
                                                       placeholder="Start date">
                                            </div>
                                            <div class="ui left icon input datepicker">
                                                <i class="calendar icon"></i>
                                                <input ref="end_date" type="text" name="search" placeholder="End date">
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="field">
                                    <div id="atrr-filters" class="ui floating labeled icon dropdown multiple button">
                                        <i class="filter icon"></i>
                                        <span class="text">Attributes (select many)</span>
                                        <div class="menu">
                                            <div class="header">
                                                <i class="tags icon"></i>
                                                Competition filters
                                            </div>
                                            <div data-value="comps_im_in" class="item">
                                                I'm in
                                            </div>
                                            <div data-value="not_closed" class="item">
                                                Has not finished
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="field">
                                    <div id="sort-filters" class="ui floating labeled icon dropdown button">
                                        <i class="filter icon"></i>
                                        <span class="text">Sorted by</span>
                                        <div class="menu">
                                            <div data-value="sort-deadline" class="item">
                                                Next deadline
                                            </div>
                                            <div data-value="sort-prize" class="item">
                                                Prize amount
                                            </div>
                                            <div data-value="sort-parts" class="item">
                                                Number of participants
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="field">
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
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="item column three wide">
                <div class="ui input">
                    <div class="ui inverted blue button">Create Competition</div>
                </div>
            </div>
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

            </div>
        </div>

        <div id="results_container" class="row centered">
            <div class="fourteen wide column">
                <div class="ui stacked">
                    <!--<search-result each="{ results }"></search-result>-->
                    <competition-tile each="{ results }" data="{ this }" class="item"
                                      show="{ display_mode === 'list' }"></competition-tile>

                    <div class="ui link cards">
                        <competition-card each="{ results }" class="ui centered card"
                                          show="{ display_mode === 'card' }"></competition-card>
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
                        if (!date) return '';
                        var day = date.getDate() + '';
                        if (day.length < 2) {
                            day = '0' + day;
                        }
                        var month = (date.getMonth() + 1) + '';
                        if (month.length < 2) {
                            month = '0' + month;
                        }
                        var year = date.getFullYear();
                        return year + '-' + month + '-' + day;
                    }
                },
                popupOptions: {
                    position: 'bottom left',
                    lastResort: 'bottom left',
                    hideOnScroll: false
                }
            })
            $(".ui.dropdown").dropdown()

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
            }, 100)
        }

        self.search = function (query) {
            //query = query || self.refs.search.value
            query = {q: self.refs.search.value}

            if (self.refs.start_date.value) {
                query.start_date = self.refs.start_date.value
            }
            if (self.refs.end_date.value)
            {
                query.end_date = self.refs.end_date.value
            }

            var attr_filters = $("#atrr-filters").dropdown('get value')

            var sort_filters = $("#sort-filters").dropdown('get value')

            var time_range_flags = $("#time-filters").dropdown('get value')

            // Grab our value above, check if it's empty, set to null. If not empty, send the value away.
            if (time_range_flags !== "")
            {
                query.date_flags = time_range_flags
            }
            else
            {
                query.date_flags = null
            }

            if (typeof attr_filters !== 'undefined' && attr_filters.length > 0)
            {
                query.attr_filters = attr_filters
            }

            if (sort_filters)
            {

            }
            else


            CHAHUB.api.search(query)
                .done(function (data) {
                    console.log(data)
                    self.update({
                        results: data.results,
                        suggestions: data.suggestions
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
    <div class="image">
        <!--<img src="https://semantic-ui.com/images/wireframe/image.png">-->
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
    </div>
</search-result>

<competition-tile>

    <div class="ui grid">
        <div class="ui middle aligned attached message stretched row main-wrapper">
            <div class="four wide column">
                <div class="ui square bordered small image">
                    <img src="https://i.imgur.com/n2XUSxU.png">
                    <!--<img src="{ logo }">-->
                </div>
            </div>
            <div class="nine wide column">
                <div class="ui row">
                    <div class="twelve wide column">
                        <h1 class="ui large header">
                            {title}
                        </h1>
                        <p style="font-size: 14px">
                            {description}
                        </p>
                    </div>
                    <div class="four wide right justify left align column">
                        <div align="right" class="content">
                            <i>Organized by: <b>{created_by}</b></i>
                        </div>
                    </div>
                </div>
                <div class="ui row">
                    <div class="sixteen wide column">
                        <div class="content">
                            <!--Tags?-->
                        </div>
                    </div>
                </div>
                <div class="ui row">
                    <div class="sixteen wide column">
                        <div class="content">
                            Tags: <b>Beginner</b>, <b>AutoML</b>
                            <br>
                            Admins: <b>tthomas63</b>
                        </div>
                    </div>
                </div>
            </div>
            <div class="three wide blue column center aligned" style="min-height: 100%">
                <i>Comp deadline:</i>
                <i>{end}</i>
                <div class="ui divider"></div>
                <i>Phase deadline:</i>
                <i>April 14 2018</i>
                <div class="ui divider"></div>
                <i>Participants: {part_count}</i>
            </div>
        </div>
    </div>

    <script>
        var self = this;

        self.one('mount', function () {
            //self.update_producers()
            self.part_count = opts.data.participants.length
            self.update()
        })

    </script>

    <style type="text/stylus">
        :scope
            display block
            margin-bottom 35px !important

        .main-wrapper
            border-left 5px solid lightgreen
            border-top-left-radius 6px !important
            border-bottom-left-radius 6px !important
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
