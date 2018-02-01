<search>
    <div class="ui top fixed secondary menu">
        <div class="ui grid container menu-holder">
            <div class="item column thirteen wide">

            </div>
            <div class="item column three wide right aligned">
                <div class="ui input inverted">
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

    <div class="ui grid container">
        <div class="row">
            <div class="column center aligned">
                <h1 style="font-size: 128px;">Chahub</h1>
            </div>
        </div>
        <div class="row">
            <div class="column wide sixteen">
                <div id="search_wrapper" class="ui fluid search focus">
                    <div class="ui icon input fluid">
                        <!--<input ref="search_field" class="prompt" type="text" placeholder="Keywords" oninput="{ input_updated }">-->
                        <input ref="search" class="prompt" type="text" placeholder="Keywords" onkeydown="{ search_key_down }">
                        <i class="search icon"></i>
                    </div>
                    <!--<div class="results transition {visible: !!suggestions && suggestions.length > 0}">
                        <a class="result" each="{ suggestions }">
                            <div class="content">
                                <div class="title">{ text } (score: { score })</div>
                            </div>
                        </a>
                    </div>-->

                    <!--<div ref="search_wrapper" class="ui fluid multiple search selection dropdown exclude-from-init">
                        <input type="hidden" name="country" value="kp">
                        <i class="search icon"></i>
                        <input ref="search_field" class="search" oninput="{ input_updated }">
                        <div class="default text">Search...</div>
                        <div class="menu">
                            <div class="item" each="{ suggestions }">{ text } (score: { score })</div>
                        </div>
                    </div>-->
                </div>
            </div>
        </div>
    </div>
    <script>
        const self = this

        self.search_key_down = function(event) {
            // enter key
            if (event.keyCode === 13) {
                self.search()
            }
        }

        self.search = function() {
            route('search/?q=' + self.refs.search.value)
        }
    </script>
</search>