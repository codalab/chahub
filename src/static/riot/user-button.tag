<user-button>
    <a id="login-button" hide="{CHAHUB.state.user.is_authenticated}" href="{URLS.LOGIN}" class="ui button">LOGIN</a>
    <span id="login-button"
          if="{CHAHUB.state.user.is_authenticated}"
          class="ui login-button dropdown button item">
        <span class="text">
            <i class="icon user outline"></i>
            {CHAHUB.state.user.username}
        </span>
        <i class="dropdown icon"></i>
        <div class="menu">
            <virtual if="{CHAHUB.state.user.is_superuser}">
                <div class="header">Administration</div>
                    <a class="item" href="{URLS.ADMIN}">Django Admin</a>
                    <a class="item" href="{URLS.PRODUCERS}">Producers</a>
                    <a class="item" href="{URLS.OAUTH}">OAuth Applications</a>
                <div class="ui divider"></div>
            </virtual>
            <div class="header">Chasuite</div>
            <a class="item" href="https://competitions.codalab.org/">Codalab</a>
            <a class="item" href="https://chagrade.lri.fr/">Chagrade</a>
            <a class="item" href="https://chalab.lri.fr/">Chalab</a>
            <a class="item" href="#">Chagle</a>
            <div class="ui divider"></div>

            <div class="header">My Account</div>
            <a class="item" href="{URLS.MY_PROFILE}"><i class="icon user"></i>My profile</a>
            <a class="item" href="{URLS.LOGOUT}"><i class="icon sign out"></i>Logout</a>
        </div>
    </span>


    <script>
        let self = this
        self.on('mount', function () {
            $('.login-button.dropdown', self.root).dropdown()
        })
    </script>
    <style type="text/stylus">
        #login-button
            position absolute
            right 20px
            top 15px
            z-index 1000
            @media screen and (max-width 767px)
                display none
            @media screen and (min-width 2560px)
                font-size 1.4rem

        .ui.button
            margin-top 10px
            color #e2e2e2
            background-color rgba(255, 255, 255, .15)
            font-weight 100

        .ui.button:hover
            color #3f3f3f
            background-color #cacbcd !important

            .icon
                opacity 1 !important
    </style>
</user-button>