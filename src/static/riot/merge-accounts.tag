<merge-accounts>
    <style>
        #particles-js {
            max-height: 10vh;
        }
    </style>
    <div id="particles-js">
        <a href="/"><img id="brand_logo" src="{URLS.STATIC('img/temp_chahub_logo_beta.png')}"></a>
    </div>

    <div style="min-height: 80% !important;" class="ui container">
        <div class="ui centered grid">
            <div class="row">
                <div class="eight wide column">
                    <div style="margin-top: 15vh;" class="ui message">
                        <h2 class="ui header">Merge two accounts</h2>
                        <div class="ui stacked center aligned segment">
                            <form class="ui form">
                                <div style="margin-top: 5vh;" class="fields">
                                    <div class="fourteen wide inline field">
                                        <label>Master Account Email:</label>
                                        <input ref="master_account" type="text">
                                    </div>
                                </div>
                                <div class="fields">
                                    <div class="fourteen wide inline field">
                                        <label>Secondary Account Email:</label>
                                        <input ref="secondary_account" type="text">
                                    </div>
                                </div>
                                <div class="ui blue button" onclick="{create_merge_request}">Send</div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        self = this;
        self.on('mount', function () {
            particlesJS.load('particles-js', "/static/particles/particles-profile.json", function () {
                console.log('callback - particles.js config loaded');
            })
        })

        self.create_merge_request = function() {
            var data = {
                'master_account': self.refs.master_account.value,
                'secondary_account': self.refs.secondary_account.value
            }
            CHAHUB.api.create_merge(data)
                .done(function (data) {
                    toastr.success("Succesfully made request!")
                })
                .fail(function (error) {
                    toastr.error("Error submitting merge request; " + error.responseJSON['error'])
                })
        }
    </script>
</merge-accounts>