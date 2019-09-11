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
                        <em>User Details Under Construction</em>
                    </div>
                </div>
            </div>
        </div>

        <!------------ ACCOUNT TAB ----------->
        <div class="ui account tab" data-tab="account" if="{opts.admin === 'True'}">
            <div class="ui grid container">
                <div class="row">
                    <div class="sixteen wide column">
                        <div class="ui form">
                            <div class="ui basic red button" onclick="{show_delete_modal}">Delete Account</div>
                            <a class="ui button" href="{URLS.MERGE_ACCOUNTS}">Merge Accounts</a>
                            <a class="ui icon button" href="{URLS.SOCIAL_BEGIN.GITHUB}"><i class="github icon"></i> Connect with GitHub</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div ref="delete_modal" class="ui modal">
        <div class="ui header">
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
    <script>
        var self = this

        self.user = {}

        self.on('mount', function () {
            $('.secondary.pointing.menu .item', self.root).tab()
            self.update_profiles()
        })

        self.show_delete_modal = function () {
            $(self.refs.delete_modal).modal('show')
        }

        self.delete_user = function () {
            if(confirm("Are you REALLY sure you want to delete this account?")) {
                CHAHUB.api.delete_user(self.opts.user_pk)
                    .done(function (data) {
                        toastr.success('Successfully Deleted User')
                        location = URLS.HOME
                    })
            }
        }

        self.update_profiles = function () {
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