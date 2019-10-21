
<show-stats>
    <button id="stats-btn" onclick="{ stats_button_clicked }"
            class="ui black big launch left attached fixed button">
        <i class="icon {minus: !show_stats, 'chart bar': show_stats}"></i>
        <span class="btn-text">Stats</span>
    </button>
    <div id="stat-card" show="{ !show_stats }" class="ui card">
        <div class="content">
            <div class="header">By the numbers...</div>
        </div>
        <div class="content">
            <h4 class="ui sub blue header">Chahub brings together</h4>
            <div class="ui two column grid">
                    <div class="column" each="{ stat in producer_stats }" no-reorder>
            <div class="ui six tiny statistics">
                <div class="statistic">
                    <div class="value">
                        { stat.count }
                    </div>
                    <div class="label">
                        { stat.label }
                    </div>
                </div>
            </div>
                </div>
            </div>

        </div>
    </div>

    <script>
        var self = this
        self.show_stats = false
        self.producer_stats = {}

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
            self.get_general_stats()
        })

        self.get_general_stats = function () {
            CHAHUB.api.get_producer_stats()
                .done(function (data) {
                    console.log("Received general stats")
                    self.update({
                        producer_stats: [
                            {label: "Competitions", count: num_formatter(data.competition_count, 1)},
                            {label: "Datasets", count: num_formatter(data.dataset_count, 1)},
                            {label: "Participants", count: num_formatter(data.participant_count, 1)},
                            {label: "Submissions", count: num_formatter(data.submission_count, 1)},
                            {label: "Users", count: num_formatter(data.user_count, 1)},
                            {label: "Organizers", count: num_formatter(data.organizer_count, 1)},
                        ],
                    })
                })
        }

        self.stats_button_clicked = function () {
            self.show_stats = !self.show_stats
            self.update()
        }
    </script>

    <style type="text/stylus">
        :scope
            position fixed

        #stats-btn
            position fixed
            top 110px
            right 0 !important
            width 55px
            height auto
            white-space nowrap
            overflow hidden
            transition 0.3s width ease, 0.5s transform ease

            .icon
                margin 0 .5em 0 -0.45em

        #stats-btn:hover
            width 130px

            .btn-text
                opacity 1

        .btn-text
            position absolute
            white-space nowrap
            top auto
            right 54px
            opacity 0
            -webkit-transition 0.23s opacity 0.2s
            -moz-transition 0.23s opacity 0.2s
            -o-transition 0.23s opacity 0.2s
            -ms-transition 0.23s opacity 0.2s
            transition 0.23s opacity 0.2s

        #stat-card
            z-index -1

        .ui.card>.content, .ui.cards>.card>.content
            padding-right 3em

        .ui.card>.content>.sub.header
            padding-bottom 10px

        .ui.statistics>.statistic
            flex 1 1 auto
    </style>
</show-stats>
