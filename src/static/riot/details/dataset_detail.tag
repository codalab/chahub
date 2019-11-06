<dataset_detail>
    <div id="dataset_detail">

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

    </style>
</dataset_detail>
