
<competition-modal>
    <div class="ui modal competition-form" ref="modal">
        <i class="close icon"></i>
        <div class="header">
            Edit Competition
        </div>
        <div style="padding: 20px;" class="edit-competition-form ui form">
            <div class="field">
                <label for="competition-title">Title</label>
                <input id="competition-title" type="text" class="ui input" ref="competition_title" name="title">
            </div>
            <div class="field">
                <label for="competition-description">Description</label>
                <textarea class="ui input" ref="competition_description" id="competition-description"
                          name="description"></textarea>
            </div>
            <div class="field">
                <label for="logo-url">Logo URL</label>
                <input type="url" class="ui input" ref="competition_logo" id="logo-url" name="logo">
            </div>
        </div>
        <div class="actions">
            <div class="ui black deny button">
                Cancel
            </div>
            <div class="ui positive right labeled icon button">
                Submit
                <i class="checkmark icon"></i>
            </div>
        </div>
    </div>

    <script>
        var self = this

        CHAHUB.events.on('competition_selected', function (competition) {
            self.selected_competition = competition
            self.refs.competition_title.value = self.selected_competition.title
            self.refs.competition_description.value = self.selected_competition.description
            self.refs.competition_logo.value = self.selected_competition.logo
            console.log(self)
            self.update()
            $(self.refs.modal).modal('show')
        })
    </script>
</competition-modal>