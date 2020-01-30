<task_detail>
    <div class="ui grid" id="task-grid">
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider"></div>
                <h2 class="ui header">{task.name}</h2>
                <h4 class="ui header">{task.description}</h4>
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Details</div>
                <div><span class="detail_name">Created By:</span> {task.created_by}</div>
                <div><span class="detail_name">Key:</span> {task.key}</div>
                <div><span class="detail_name">Producer:</span> {_.get(task.producer, 'name')}</div>
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Datasets</div>
                <div if="{task.ingestion_program}">
                    <span class="detail_name">Ingestion Program:</span>
                    <a href="{URLS.DATASET_DETAIL(task.ingestion_program.id)}" target="_blank">{task.ingestion_program.name || 'Name Not Available'}</a>
                </div>
                <div if="{task.scoring_program}">
                    <span class="detail_name">Scoring Program:</span>
                    <a href="{URLS.DATASET_DETAIL(task.scoring_program.id)}" target="_blank">{task.scoring_program.name || 'Name Not Available'}</a>
                </div>
                <div if="{task.input_data}">
                    <span class="detail_name">Input Data:</span>
                    <a href="{URLS.DATASET_DETAIL(task.input_data.id)}" target="_blank">{task.input_data.name || 'Name Not Available'}</a>
                </div>
                <div if="{task.reference_data}">
                    <span class="detail_name">Reference Data:</span>
                    <a href="{URLS.DATASET_DETAIL(task.reference_data.id)}" target="_blank">{task.reference_data.name || 'Name Not Available'}</a>
                </div>
            </div>
        </div>
    </div>

    <script>
        let self = this
        self.task = {}

        self.on('mount', function () {
            CHAHUB.api.get_task(self.opts.pk)
                .done(data => {
                    self.task = data
                    self.update()
                    console.log(data)
                })
                .fail(() => {
                    toastr.error('Could not retrieve task')
                })
        })
    </script>
    <style type="text/stylus">

    </style>
</task_detail>
