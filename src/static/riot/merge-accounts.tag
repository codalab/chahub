<merge-accounts>
    <div id="particles-js">
        <a href="/"><img id="brand_logo" src="{URLS.STATIC('img/temp_chahub_logo_beta.png')}"></a>
    </div>

    <div style="" class="ui container account-merge-container">
        <div class="ui centered grid">
            <div class="row">
                <div class="eight wide column">
                    <div style="" class="ui message account-merge-message">
                        <h2 class="ui header">Merge two accounts</h2>
                        <div class="ui stacked center aligned segment">
                            <form class="ui form">
                                <div style="" class="fields account-merge-field">
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
    <style>
        #particles-js {
            max-height: 10vh;
        }

        .account-merge-container {
            min-height: 80% !important;
        }

        .account-merge-message {
            margin-top: 15vh !important;
        }

        .account-merge-field {
            margin-top: 5vh !important;
        }
    </style>

    <script>
        var self = this;
        self.on('mount', function () {
            particlesJS.load('particles-js', "/static/particles/particles-profile.json", function () {})
        })

        self.create_merge_request = function() {
            var data = {
                master_account: self.refs.master_account.value,
                secondary_account: self.refs.secondary_account.value
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