<search-results>
    <div class="ui top fixed menu">
        <div class="ui grid container menu-holder">
            <div class="item column thirteen wide">
                <div class="ui icon input">
                    <input type="text" placeholder="Search..." ref="search" onkeydown="{ input_updated }">
                    <i class="search icon"></i>
                </div>
            </div>
            <div class="item column three wide">
                <div class="ui input">
                    <div class="ui primary button">Create Competition</div>
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
                <div class="ui form">
                    <div class="inline fields">
                        <div class="field">
                            <div id="time-range" class="ui floating labeled icon dropdown button">
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
                                        <input type="text" name="search" placeholder="Start date">
                                    </div>
                                    <div class="ui left icon input datepicker">
                                        <i class="calendar icon"></i>
                                        <input type="text" name="search" placeholder="End date">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="field">
                            <div class="ui floating labeled icon dropdown multiple button">
                                <i class="filter icon"></i>
                                <span class="text">Attributes (select many)</span>
                                <div class="menu">
                                    <div class="header">
                                        <i class="tags icon"></i>
                                        Competition filters
                                    </div>
                                    <div class="item">
                                        I'm in
                                    </div>
                                    <div class="item">
                                        Has not finished
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="field">
                            <div class="ui floating labeled icon dropdown button">
                                <i class="filter icon"></i>
                                <span class="text">Sorted by</span>
                                <div class="menu">
                                    <div class="item">
                                        Next deadline
                                    </div>
                                    <div class="item">
                                        Prize amount
                                    </div>
                                    <div class="item">
                                        Number of participants
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="results_container" class="row centered">
            <div class="twelve wide column">
                <div class="ui divided stacked items">
                    <search-result each="{ results }"></search-result>
                    <div class="item" show="{ results.length == 0 }">
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

        self.on('mount', function () {
            /*$(self.refs.search_wrapper).dropdown({


             on results do


             onNoResults: function(search) {}
             })*/
            // Template stuff
            $('.datepicker').calendar({
                type: 'date',
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
            if(!!params.q) {
                self.search(params.q)
                self.refs.search.value = params.q
            }
        })

        self.input_updated = function () {
            delay(function () {
                self.search()
            }, 100)
        }

        self.search = function (query) {
            query = query || self.refs.search.value
            CHAHUB.api.search(query)
                .done(function (data) {
                    console.log(data)
                    self.update({
                        results: data.results,
                        suggestions: data.suggestions
                    })
                })
        }
    </script>

    <style type="text/stylus">
        #results_container
            min-height 375px

        #search_wrapper .results
            margin-top 1px

        .ui.button:hover .icon
            opacity 1
    </style>
</search-results>

<search-result class="item">
    <div class="image">
        <img src="https://semantic-ui.com/images/wireframe/image.png">
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