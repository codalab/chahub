<competition_detail>
    <div class="ui grid">
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider"></div>
                <h2 class="ui header">{competition.title}</h2>
                <h4 class="ui header">{competition.description}</h4>
                <a href="{competition.url}">{competition.url}</a>

            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Details</div>
                <div><span class="detail_name">Start:</span> {pretty_date(competition.start)}</div>
                <div><span class="detail_name">End:</span> {pretty_date(competition.end) || "Never"}</div>
                <div><span class="detail_name">Created By:</span> {competition.created_by}</div>
                <div><span class="detail_name">Producer:</span> {_.get(competition.producer, 'name')}</div>
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Statistics</div>
                <div class="ui two mini statistics">
                    <div class="ui statistic">
                        <div class="value">{competition.participant_count}</div>
                        <div class="label">Participants</div>
                    </div>
                    <div class="ui statistic">
                        <div class="value">0</div>
                        <div class="label">Submissions</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Phases</div>
                <div class="ui fluid styled accordion">
                    <virtual each="{phase in competition.phases}">
                        <div class="title {active: phase.index === 0}">
                            <i class="dropdown icon"></i>
                            {phase.name}
                        </div>
                        <div class="content {active: phase.index === 0}">
                            <p><span class="detail_name">Description:</span> {phase.description}</p>
                            <p><span class="detail_name">Start:</span> {pretty_date(phase.start)}</p>
                            <p><span class="detail_name">End:</span> {pretty_date(phase.end)}</p>
                            <p><span class="detail_name">Status:</span> {phase.status || "None"}</p>
                        </div>
                    </virtual>
                </div>
            </div>
        </div>
    </div>


    <script>
        let self = this
        self.competition = {}

        self.on('mount', function () {
            CHAHUB.api.get_competition(self.opts.pk)
                .done(data => {
                    self.competition = data
                    self.update()
                    $('.ui.accordion', self.root).accordion()
                    console.log(data)
                })
                .fail(() => {
                    toastr.error('Could not retrieve competition')
                })
        })
    </script>

    <style type="text/stylus">
        .detail_name
            color #2a4457
            font-weight bold
            font-size medium
    </style>
</competition_detail>
