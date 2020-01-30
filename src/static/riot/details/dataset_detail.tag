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
            </div>
        </div>
        <div class="row">
            <div class="ui sixteen wide column">
                <a href="{dataset.download_url}" class="ui green icon button"><i class="download icon"></i> Download</a>
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
</dataset_detail>
