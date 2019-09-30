<merge-accounts>
    <div class="ui centered grid container account-merge-container">
        <div class="row">
            <div class="fourteen wide column">
                <div class="ui grid message account-merge-segment">

                    <div class="row">
                        <div class="six wide column">
                            <h3 class="ui header form-header">
                                Account Merge Request
                            </h3>
                            <div class="ui success message" show="{message}">
                                <div class="header">Success</div>
                                <p>
                                    {message}<br>
                                    Return <a href="/">Home</a>.
                                </p>
                            </div>
                            <div class="ui error message" show="{!_.isEmpty(errors)}">
                                <div class="header">
                                    Error
                                </div>
                                <p> {errors} </p>
                            </div>
                            <form class="ui form {loading: loading}" onsubmit="{confirm_merge}">
                                <div class="field">
                                    <div class="ui left icon input">
                                        <i class="envelope icon"></i>
                                        <input ref="master_account"
                                               placeholder="Master Account Email"
                                               type="email"
                                               required>
                                    </div>
                                </div>
                                <div class="field">
                                    <div class="ui left icon input">
                                        <i class="envelope outline icon"></i>
                                        <input ref="secondary_account"
                                               placeholder="Secondary Account Email"
                                               type="email"
                                               required>
                                    </div>
                                </div>
                                <button class="ui blue fluid submit button">Submit</button>
                            </form>
                        </div>
                        <div class="ten wide column explanation-column">
                            <h4>Please enter the primary email addresses of the two accounts you want to merge</h4>
                            <p>After submitting a merge request, emails will be sent to <em>both</em> email addresses
                                with a link to confirm the merge request. When both email addresses have verified the
                                merge
                                request, all of the relevant information from the secondary account will be merged in to
                                the master account. The secondary account will then be removed.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="ui small modal" ref="modal">
        <div class="header">
            Please confirm your merge request.
        </div>
        <div class="content">
            <p>Emails will be sent to both email addresses to confirm this merge. When both email accounts
                have validated this merge request, it will be executed.</p>

            <p>All the email addresses, GitHub information, profiles, and profile associated data will
                be removed from the secondary account (<a>{_.get(merge_data, 'secondary_account')}</a>) and added to
                the master account (<a>{_.get(merge_data, 'master_account')}</a>). The secondary account will no longer
                exist. You will log in with the credentials of the master account.</p>
        </div>
        <div class="actions">
            <div class="ui cancel button">Cancel</div>
            <div class="ui submit green button" onclick="{create_merge_request}">Confirm</div>
        </div>
    </div>

    <script>
        var self = this
        self.errors = []
        self.merge_data = {}
        self.loading = false

        self.on('mount', function () {
            self.message = self.opts.message
            self.update()
            $(self.refs.modal).modal({
                onHidden: function () {
                    self.merge_data = {}
                    self.update()
                }
            })
        })

        self.clear_form = function () {
            self.refs.master_account.value = ''
            self.refs.secondary_account.value = ''
            self.errors = []
            self.update()
        }

        self.confirm_merge = function (e) {
            e.preventDefault()
            self.merge_data = {
                master_account: self.refs.master_account.value,
                secondary_account: self.refs.secondary_account.value
            }
            self.update()
            $(self.refs.modal).modal('show')

        }

        self.create_merge_request = function () {
            $(self.refs.modal).modal('hide')
            self.loading = true
            self.update()
            CHAHUB.api.create_merge(self.merge_data)
                .done(function (data) {
                    self.clear_form()
                    toastr.success("Successfully made request!")
                })
                .fail(function (error) {
                    error = error.responseJSON
                    self.errors = _.uniq(_.flatten(_.values(error)))
                    self.update()
                })
                .always(function () {
                    self.loading = false
                    self.update()
                })
        }
    </script>

    <style scoped type="text/stylus">
        .account-merge-container
            min-height 85vh !important

        .account-merge-segment
            margin-top 5vh !important

        .explanation-column
            border-left 1px solid #cacaca

        .form-header
            padding-bottom 10px !important

    </style>
</merge-accounts>