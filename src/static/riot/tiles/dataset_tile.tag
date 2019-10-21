<dataset-tile>
    <div class="floating-actions { is-admin: CHAHUB.state.user.is_superuser }">
        <i class="icon green pencil alternate"></i>
        <i class="icon red delete"></i>
        <i class="icon { yellow: opts.dataset.locked, unlock: opts.dataset.locked, lock: !opts.dataset.locked }"></i>
    </div>
    <div class="ui tiny image">
        <h5 class="ui icon header">
            <i class="file archive outline icon"></i>
        </h5>
    </div>
    <div class="content">
        <div class="header">
            { opts.dataset.name }
        </div>
        <div class="description">
            <p>{opts.dataset.description}</p>
        </div>
    </div>
    <script>
        let self = this
    </script>
    <style type="text/stylus">
        :scope
            display block
            position relative

        :scope:hover .floating-actions.is-admin
            opacity 1

        .floating-actions
            position absolute
            top 0
            right 0
            opacity 0
            z-index 10

        .content
            .description
                margin-top 0 !important
                color #808080 !important
                display block
                font-size .9em !important

            p
                line-height 1.1em !important

            @media screen and (max-width 645px)
                padding-left 0.8em !important

        .extra
            margin-top 0
            @media screen and (max-width 749px)
                margin-bottom 0 !important

            .url
                font-size .8em
                color rgba(0, 0, 255, 0.6) !important
                white-space nowrap
                overflow hidden
                text-overflow ellipsis
                max-width 90vw
                display block !important
                @media screen and (min-width 2560px)
                    margin-bottom: 10px;
                    overflow: visible;
                @media screen and (max-width 750px) {
                    margin-bottom: -6px;
                }

            .date
                font-size 0.8em
                color #8c8c8c !important

        .ui.avatar.image
            max-width 4em
            @media screen and (max-width 750px)
                max-width 3em
            @media screen and (min-width 2560px)
                max-width 8em

        .ui.image
            max-width 60px
            display inline-grid !important
            justify-content center
            @media screen and (min-width 2560px)
                max-width 240px

        .participant_label
            background-color #475e6f !important
            border-color #475e6f !important
            color #dfe3e5 !important
            right 0
            margin 0 2px !important
            text-align right

            .icon
                float left

        .prize_label
            background-color rgba(99, 84, 14, 0.68) !important
            border-color rgba(99, 84, 14, 0.68) !important
            color #dee2e4 !important
            margin 0 2px !important

        .deadline_label
            margin 0 2px !important

        .mobile_linewrap
            white-space nowrap
            overflow hidden
            text-overflow ellipsis
            color rgba(0, 0, 255, 0.6)
            margin-bottom 5px !important
            margin-right 0 !important

        .label
            @media screen and (min-width 2560px)
                font-size 1.2rem !important

        .mobile_labelwrap
            display block
            @media screen and (min-width 500px)
                display inline-block

        @media screen and (min-width 2560px)
            *
                font-size 1.5rem !important

            .header
                font-size 2rem !important
    </style>
</dataset-tile>