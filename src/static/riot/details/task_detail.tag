<task_detail>
    <div id="task_detail">

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
