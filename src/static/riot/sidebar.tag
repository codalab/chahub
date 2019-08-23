<sidebar class="ui thin sidebar right inverted vertical overlay menu">
    <a id="login-button" hide="{SITE.state.user.is_authenticated}" style="" href="/accounts/login/"
       class="item">LOGIN</a>
    <a id="login-button" show="{SITE.state.user.is_authenticated}" style="" href="/accounts/logout/"
       class="item">LOGOUT</a></a>

    <style scoped>
        :scope {
            display: block;
        }
    </style>
</sidebar>
