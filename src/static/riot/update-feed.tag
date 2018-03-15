<update-feed>
    <ul>
        <li each="{competitions}">{title} hosted at {producer.url}</li>
    </ul>
    <script>
        var self = this
        self.competitions = []

        CHAHUB.events.on('competition_update', function(data){
            self.competitions.push(data)
            self.update()
        })
    </script>
</update-feed>