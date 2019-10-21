<competition-tile>
    <div class="floating-actions { is-admin: CHAHUB.state.user.is_superuser }">
        <i class="icon green pencil alternate"
           onclick="{ edit_competition }"></i>
        <i class="icon red delete" onclick="{ delete_competition }"></i>
        <i class="icon { yellow: opts.comp.locked, unlock: opts.comp.locked, lock: !opts.comp.locked }" onclick="{ lock_competition}"></i>
    </div>
    <div class="ui tiny image">
        <img src="{opts.comp.logo || URLS.STATIC('img/img-wireframe.png')}" class="ui avatar image">
    </div>
    <div class="content">
        <div class="header">
            {opts.comp.title}
        </div>
        <div class="description">
            <p>{opts.comp.description}</p>
        </div>
        <div class="extra">
            <div class="mobile_linewrap">
                <span class="url"><a href="{opts.comp.url}">{url_short(opts.comp.url)}</a></span>
                <span class="date">
                {pretty_date(opts.comp.start)}
                <virtual if="{opts.comp.end}">
                    - {pretty_date(opts.comp.end)}
                </virtual>
            </span>
                <div class="mobile_labelwrap"></div>
                <span class="participant_label ui right floated mini label tooltip" data-content="Participant count">
                    <i class="user icon"></i> {opts.comp.participant_count}
                </span>
                <span class="deadline_label ui right floated mini label tooltip {red: !opts.comp.alert_icon}"
                      data-content="Deadline of the current phase"
                      show="{opts.comp.current_phase_deadline}">
                    <i show="{!opts.comp.alert_icon}" class="alarm icon"></i> {opts.comp.pretty_deadline_time}
                </span>
                <span class="deadline_label ui right floated mini label" show="{!opts.comp.current_phase_deadline}">
                    Never ends
                </span>
                <span class="prize_label ui right floated mini label tooltip" data-content="Prize Amount"
                      show="{opts.comp.prize}">
                    <i class="yellow trophy icon"></i> {opts.comp.prize}
                </span>
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
            $(self.refs.modal).modal()
        })

        self.redirect_to_url = function () {
            window.open(self.url, '_blank');
        }

        self.url_short = function (url) {
            return url.replace(/^(?:https?:\/\/)?(?:www\.)?/i, "").split('/')[0];
        }

        self.edit_competition = function (event) {
            CHAHUB.events.trigger('competition_selected', event.item)
            event.cancelBubble = true
        }

        self.delete_competition = function (event) {
            // TODO - Need to delete the competition on confirm, else do nothing.
            if (confirm(`Are you sure you want to delete "${event.item.title}?"`)) {
                alert('Deleted')
            }
            event.cancelBubble = true
        }

        self.lock_competition = function (event) {
            // TODO - Need to lock the competition and change icon/color to represent locked and unlocked state
            event.cancelBubble = true
        }
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
</competition-tile>
