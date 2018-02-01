<!-- Field class on initial definition to keep Semantic UI styling -->
<field class="field">
    <div class="field {error: opts.error}">
        <label>{opts.name}</label>
        <input type="text" name="{ opts.input_name }" ref="input">
    </div>
    <div class="ui error message" show="{ opts.error }">
        <p>{ opts.error }</p>
    </div>
    <style>
        /* Make this component "div like" */
        :scope {
            display: block;
        }
    </style>
</field>

<producer-management>
    <!-- Top buttons -->
    <div class="ui right aligned grid">
        <div class="sixteen wide column">
            <button class="ui green button" onclick="{ add }">
                <i class="add square icon"></i> Add new producer
            </button>
        </div>
    </div>

    <!-- Table -->
    <table class="ui table stackable">
        <thead>
        <tr>
            <th>Name</th>
            <th>Contact</th>
            <th>URL</th>
            <th class="center aligned two wide">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr each="{ producer in producers }">
            <td>{ producer.name }</td>
            <td>{ producer.contact }</td>
            <td><a href="{ producer.url }">{ producer.url }</a></td>
            <td class="center aligned">
                <div class="ui small basic icon buttons">
                    <button class="ui button" onclick="{ edit.bind(this, producer) }"><i class="edit icon"></i></button>
                    <button class="ui button" onclick="{ delete.bind(this, producer) }"><i class="red delete icon"></i></button>
                </div>
            </td>
        </tr>
        </tbody>
    </table>

    <!-- Form modal -->
    <div id="producer_form_modal" class="ui modal">
        <div class="header">Producer form</div>
        <div class="content">
            <form id="producer_form" class="ui form error" onsubmit="{ save }">
                <field name="Name" ref="name" input_name="name" error="{errors.name}"></field>
                <field name="Contact Email" ref="contact" input_name="contact" error="{errors.contact}"></field>
                <field name="URL" ref="url" input_name="url" error="{errors.url}"></field>
            </form>
        </div>
        <div class="actions">
            <input type="submit" class="ui button" form="producer_form" value="Save"/>
            <div class="ui cancel button">Cancel</div>
        </div>
    </div>

    <!-- New key modal -->
    <div id="producer_secret_key_modal" class="ui modal">
        <div class="header">Secret key</div>
        <div class="content">
            <div class="ui grid">
                <div class="column sixteen wide center aligned">
                    <h3 class="ui center aligned header">{secret_key}</h3>
                    <p class="ui center aligned">Send this key to the producer, it will not be revealed again.</p>
                </div>
            </div>
        </div>
        <div class="actions">
            <div class="ui cancel red button">I've copied down this key</div>
        </div>
    </div>

    <script>
        // --------------------------------------------------------------------
        // Initializers
        var self = this
        self.selected_producer = {}
        self.errors = []

        // --------------------------------------------------------------------
        // Events
        self.one('mount', function () {
            self.update_producers()
        })

        // --------------------------------------------------------------------
        // Helpers
        self.update_producers = function () {
            CHAHUB.api.get_producers()
                .done(function (data) {
                    self.update({producers: data})
                })
                .fail(function (error) {
                    toastr.error("Error fetching producers: " + error.statusText)
                })
        }

        self.add = function () {
            $("#producer_form_modal").modal('show')

            // We want to unselect the existing producer, so when we save we don't try to update it
            self.selected_producer = {}
        }

        self.edit = function (producer) {
            self.selected_producer = producer

            // We have to use our references to the custom <fields> to get their references to
            // the inputs!
            // Example for name:
            // <field ref="name"> -> <input ref="input">
            self.refs.name.refs.input.value = producer.name
            self.refs.contact.refs.input.value = producer.contact
            self.refs.url.refs.input.value = producer.url

            self.update()

            $("#producer_form_modal").modal('show')
        }

        self.save = function (save_event) {
            // Stop the form from propagating
            save_event.preventDefault()

            var data = $("#producer_form").serializeObject()
            var endpoint = undefined  // we'll pick form create OR update for the endpoint

            if (!self.selected_producer.id) {
                endpoint = CHAHUB.api.create_producer(data)
            } else {
                endpoint = CHAHUB.api.update_producer(self.selected_producer.id, data)

                self.selected_producer = {}
            }

            endpoint
                .done(function (data) {
                    toastr.success("Successfully saved producer")

                    self.update_producers()

                    $("#producer_form_modal").modal('hide')

                    $("#producer_form")[0].reset();

                    if (data.api_key) {
                        // We received a secret key, so we must have made a new producer. Show the
                        // key so it can be copied down
                        $("#producer_secret_key_modal").modal('show')
                        self.update({secret_key: data.api_key})
                    }
                })
                .fail(function (response) {
                    if (response) {
                        var errors = JSON.parse(response.responseText);

                        // Clean up errors to not be arrays but plain text
                        Object.keys(errors).map(function (key, index) {
                            errors[key] = errors[key].join('; ')
                        })

                        self.update({errors: errors})
                    }
                })
        }

        self.delete = function (producer) {
            if (confirm("Are you sure you want to delete this?")) {
                CHAHUB.api.delete_producer(producer.id)
                    .done(function () {
                        toastr.success("Deleted!")
                        self.update_producers()
                    })
                    .fail(function (response) {
                        toastr.error("Could not delete.\n\n" + response.responseText)
                    })
            }
        }
    </script>
</producer-management>
