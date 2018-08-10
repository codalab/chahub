<sidebar class="ui thin sidebar right inverted vertical overlay menu">
    <a id="login-button" hide="{USER_AUTHENTICATED}" style="" href="/accounts/login/"
       class="item">LOGIN</a>
    <a id="login-button" show="{USER_AUTHENTICATED}" style="" href="/accounts/logout/"
       class="item">LOGOUT</a></a>

    <style scoped>
        :scope {
            display: block;
        }
    </style>
</sidebar>
