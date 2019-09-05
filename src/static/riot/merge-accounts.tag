<merge-accounts>
    <div class="ui container account-merge-container">
        <div class="ui centered grid">
            <div class="row">
                <div class="eight wide column">
                    <div class="ui message account-merge-message">
                        <h2 class="ui header">Merge two accounts</h2>
                        <div class="ui center aligned segment">
                            <div class="ui error message" show="{!_.isEmpty(errors)}">
                                <div class="header">
                                    Form Errors:
                                </div>
                                <ul class="list">
                                    <li each="{error in errors}">
                                        {error}
                                    </li>
                                </ul>
                            </div>
                            <form class="ui form" onsubmit="{create_merge_request}">
                                <div class="fields account-merge-field">
                                    <div class="inline sixteen wide field {error: _.includes(error_fields, 'master_account')}">
                                        <label>Master Account Email:</label>
                                        <input ref="master_account" type="text">
                                    </div>
                                </div>
                                <div class="fields">
                                    <div class="inline sixteen wide field {error: _.includes(error_fields, 'secondary_account')}">
                                        <label>Secondary Account Email:</label>
                                        <input ref="secondary_account" type="text">
                                    </div>
                                </div>
                                <button class="ui blue submit button">Send</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        var self = this
        self.errors = []
        self.error_fields = []
        self.create_merge_request = function (e) {
            e.preventDefault()
            let data = {
                master_account: self.refs.master_account.value,
                secondary_account: self.refs.secondary_account.value
            }

            CHAHUB.api.create_merge(data)
                .done(function (data) {
                    toastr.success("Successfully made request!")
                })
                .fail(function (error) {
                    error = error.responseJSON
                    self.error_fields = _.keys(error)
                    self.errors = _.map(_.flatten(_.values(error)), error => error.replace('Object', 'User'))
                    self.update()
                    toastr.error("Error submitting merge request")
                })
        }
    </script>

    <style scoped>
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
</merge-accounts>