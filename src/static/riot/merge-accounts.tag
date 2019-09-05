<merge-accounts>
    <div class="ui container account-merge-container">
        <div class="ui centered grid">
            <div class="row">
                <div class="eight wide column">
                    <div class="ui message account-merge-message">
                        <h2 class="ui header">Merge two accounts</h2>
                        <div class="ui success message" show="{message}">
                            <div class="header">
                                Success
                            </div>
                            <p>
                                Accounts successfully merged.<br>
                                Return <a href="/">Home</a>.
                            </p>
                        </div>
                        <div class="ui center aligned segment" show="{!message}">
                            <div class="ui error message" show="{!_.isEmpty(errors)}">
                                <div class="header">
                                    Form Errors
                                </div>
                                <ul class="list">
                                    <li each="{error in errors}">
                                        {error}
                                    </li>
                                </ul>
                            </div>

                            <form class="ui form" onsubmit="{create_merge_request}">
                                <div class="fields account-merge-field">
                                    <div class="inline sixteen wide field">
                                        <label>Master Account Email:</label>
                                        <input ref="master_account" type="text">
                                    </div>
                                </div>
                                <div class="fields">
                                    <div class="inline sixteen wide field">
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

        self.on('mount', function () {
            self.message = self.opts.message
            self.update()
        })

        self.clear_form = function () {
            self.refs.master_account.value = ''
            self.refs.secondary_account.value = ''
            self.errors = []
            self.update()
        }

        self.create_merge_request = function (e) {
            e.preventDefault()
            let data = {
                master_account: self.refs.master_account.value,
                secondary_account: self.refs.secondary_account.value
            }

            CHAHUB.api.create_merge(data)
                .done(function (data) {
                    self.clear_form()
                    toastr.success("Successfully made request!")
                })
                .fail(function (error) {
                    console.log(error)
                    error = error.responseJSON
                    self.errors = _.uniq(_.flatten(_.values(error)))
                    self.update()
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