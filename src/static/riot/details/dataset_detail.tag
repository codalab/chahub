<dataset_detail>
<div class="ui grid">
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider"></div>
                <h2 class="ui header">{dataset.name}</h2>
                <h4 class="ui header">{dataset.description}</h4>
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <div class="ui horizontal divider">Details</div>
                <div><span class="detail_name">Created By:</span> {dataset.created_by}</div>
                <div><span class="detail_name">Key:</span> {dataset.key}</div>
                <div><span class="detail_name">Producer:</span> {_.get(dataset.producer, 'name')}</div>
                <div><span class="detail_name">In Use:</span> {_.isEmpty(dataset.tasks_using) ? 'No' : 'Yes'}</div>
            </div>
        </div>
    </div>

    <script>
        let self = this
        self.dataset = {}

        self.on('mount', function () {
            CHAHUB.api.get_dataset(self.opts.pk)
                .done(data => {
                    self.dataset = data
                    self.update()
                    console.log(data)
                })
                .fail(() => {
                    toastr.error('Could not retrieve dataset')
                })
        })
    </script>
    <style type="text/stylus">
        .detail_name
            color #2a4457
            font-weight bold
            font-size medium
    </style>
</dataset_detail>
