<profile-page>
    <div class="ui container">
        <user-button></user-button>
        <div class="ui profile-segment segment">
            <div class="ui container profile-header">
                <div class="holder">
                    <img src="{ _.get(user, 'github_user_info.avatar_url', URLS.STATIC('img/img-wireframe.png')) }"
                         class="profile-img" alt="profile-image">
                </div>
                <div class="profile-user">
                    { _.get(user, 'username', 'Anonymous / N/A') }
                    <div show="{ _.get( user, 'github_user_info', false) }" class="profile-brief">
                        <div class="location">
                            { _.get(user, 'github_user_info.location', '') }
                        </div>
                        <div class="occupation">
                            { _.get(user, 'github_user_info.company', '') }
                        </div>
                        { _.get(user, 'github_user_info.bio', '') }
                    </div>
                    <div class="social-buttons">
                        <a href="{ _.get(user, 'github_user_info.html_url', '') }"
                           show="{ _.get(user, 'github_user_info.html_url') }"
                           class="ui circular github plus mini icon button">
                            <i class="github icon"></i>
                        </a>
                    </div>
                </div>
            </div>
            <div id="profile-menu" class="ui secondary pointing menu">
                <a class="active item" data-tab="details">
                    Details
                </a>
                <a class="item" data-tab="account" if="{opts.admin === 'True'}">
                    Account
                </a>
            </div>
        </div>

        <!------------ DETAILS TAB ----------->
        <div class="ui active details tab" data-tab="details">
            <div class="ui grid container">
                <div class="row">
                    <div class="sixteen wide column">
                        <h3>Profiles</h3>
                        <table class="ui table">
                            <thead>
                            <tr>
                                <th>Username</th>
                                <th>Producer</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr each="{profile in _.get(user, 'profiles', [])}">
                                <td>{profile.username}</td>
                                <td>{profile.producer}</td>
                            </tr>
                            <tr if="{_.isEmpty(_.get(user, 'profiles'))}">
                                <td colspan="2" class="center aligned"><em>No Profiles Yet!</em></td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!------------ ACCOUNT TAB ----------->
        <div class="ui account tab" data-tab="account" if="{opts.admin === 'True'}">
            <div class="ui grid container">
                <div class="row">
                    <table class="ui celled table">
                        <thead>
                        <tr>
                            <th>Email Address</th>
                            <th>Primary</th>
                            <th>Verified</th>
                            <th>Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr each="{email in _.get(user, 'email_addresses', [])}">
                            <td>{email.email}</td>
                            <!--TODO add icons here instead of "*"-->
                            <td>{ email.primary ? "*" : "" }</td>
                            <td>{ email.verified ? "*" : "" }</td>
                            <td>
                                <div if="{!email.verified}" class="ui button" onclick="{resend_verification_email.bind(this, email.id)}">Resend Email</div>
                                <div if="{!email.primary}" class="ui red button" onclick="{delete_email.bind(this, email.id)}">Delete Email</div>
                                <div if="{!email.primary && email.verified}" class="ui blue button" onclick="{make_primary_email.bind(this, email.id)}">Make Primary Email</div>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div class="row">
                    <div class="sixteen wide column">
                        <div class="ui form">
                            <a class="ui small icon button" href="{URLS.SOCIAL_BEGIN.GITHUB}"><i class="github icon"></i> Connect with GitHub</a>
                            <a class="ui small button" href="{URLS.MERGE_ACCOUNTS}">Merge Accounts</a>
                            <div class="ui small button" onclick="{show_email_modal}">Add Email Address</div>
                            <div class="ui small right floated basic red button" onclick="{show_delete_modal}">Delete Account</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div ref="delete_modal" class="ui modal">
        <div class="header">
            Delete Account?
        </div>
        <div class="content">
            Are you sure you want to delete your account? This cannot be undone! <br>
            If this is a duplicate account, consider <a href="{URLS.MERGE_ACCOUNTS}">merging</a> it instead.
        </div>
        <div class="actions">
            <div class="ui basic small red button" onclick="{delete_user}">Delete Account</div>
            <div class="ui small cancel button">Cancel</div>
        </div>
    </div>

    <div ref="email_modal" class="ui mini modal">
        <div class="header">
            Add Email Address
        </div>
        <div class="content">
            <form class="ui form" onsubmit="{add_email}">
                <div class="ui field">
                    <label>Email Address</label>
                    <input type="email" placeholder="user@example.com" ref="email_address">
                </div>
            </form>
        </div>
        <div class="actions">
            <div class="ui small cancel button">Cancel</div>
            <div class="ui small green submit button">Submit</div>
        </div>
    </div>
    <script>
        var self = this

        self.user = {}

        self.on('mount', function () {
            $('.secondary.pointing.menu .item', self.root).tab()
            self.update_user()
            $(self.refs.email_modal).modal({
                onHidden: function () {
                    $(self.refs.email_address).val('')
                }
            })
        })

        self.show_delete_modal = function () {
            $(self.refs.delete_modal).modal('show')
        }

        self.show_email_modal = function () {
            $(self.refs.email_modal).modal('show')
        }

        self.add_email = function (data) {
            data.preventDefault()
            let email_address = $(self.refs.email_address).val()
            if (email_address) {
                CHAHUB.api.add_email(self.opts.user_pk, email_address)
                    .done(function (data) {
                        toastr.success('Email address added. A verification email has been sent')
                        self.update_user()
                    })
                    .fail(function (response) {
                        toastr.error('Could not add email address')
                    })

            }

            $(self.refs.email_modal).modal('hide')
        }

        self.delete_email = function (email_pk) {
            if (confirm('Are you sure you want to delete this email address?')) {
                CHAHUB.api.delete_email(self.opts.user_pk, email_pk)
                    .done(function () {
                        toastr.success('Email address deleted')
                        self.update_user()
                    })
                    .fail(function () {
                        toastr.error('Could not delete email address')
                    })
            }
        }

        self.make_primary_email = function (email_pk) {
            if (confirm("Are you sure you want to make this your primary email account?")) {
                CHAHUB.api.make_primary_email(self.opts.user_pk, email_pk)
                    .done(function () {
                        toastr.success('Primary Account Changed')
                        self.update_user()
                    })
                    .fail(function () {
                        toastr.error('Error changing primary email')
                    })
            }
        }

        self.resend_verification_email = function (email_pk) {
            CHAHUB.api.resend_verification_email(self.opts.user_pk, email_pk)
                .done(function () {
                    toastr.success('Email sent!')
                })
                .fail(function () {
                    toastr.error('Could not resend email')
                })
        }

        self.delete_user = function () {
            CHAHUB.api.delete_user(self.opts.user_pk)
                .done(function (data) {
                    toastr.success('Successfully Deleted User')
                    location = URLS.HOME
                })
        }

        self.update_user = function () {
            CHAHUB.api.get_user(self.opts.user_pk)
                .done(function (data) {
                    self.user = data
                    self.update()
                    CHAHUB.events.trigger("profile_loaded", self.user)
                })
                .fail(function (response) {
                    toastr.error("Failed to retrieve profile: " + self.opts.objects[0])
                })
        }
    </script>

    <style type="text/stylus">
        #login-button
            position absolute
            right 20px
            top 15px
            z-index 10
            @media screen and (max-width 767px)
                display none
            @media screen and (min-width 2560px)
                font-size 1.4rem
            margin-top 10px
            color #e2e2e2
            background-color rgba(255, 255, 255, .15)
            font-weight 100

        #login-button:hover
            color #3f3f3f

            .icon
                opacity 1 !important

        .circular.github.button
            background-color #582c80
            color white

        .details
            margin 0 -1em

        .details > .container
            margin-top 1em

        .details > .container > .ui.segment
            width 47.5%
            margin 1em
            padding 0


        .competition-segment .flex-content
            flex-direction column
            margin 0
            padding 1em !important

    </style>
</profile-page>