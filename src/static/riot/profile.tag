<profile-page>
    <div id="particles-js">
        <a href="/"><img id="brand_logo" src="{URLS.STATIC('img/temp_chahub_logo_beta.png')}"></a>
    </div>

    <div class="ui container">
        <div class="ui profile-segment segment">
            <div class="ui container profile-header">
                <div class="holder">
                    <img src="{ _.get(profile_data, 'user.github_info.avatar_url', URLS.STATIC('img/img-wireframe.png')) }"
                         class="profile-img" alt="profile-image">
                </div>
                <div class="profile-user">
                    { _.get(profile_data, 'user.username', 'Anonymous / N/A') }
                    <div show="{ _.get( profile_data, 'github_info', false) }" class="profile-brief">
                        <div class="location">
                            { _.get(profile_data, 'github_info.location', '') }
                        </div>
                        <div class="occupation">
                            { _.get(profile_data, 'github_info.company', '') }
                        </div>
                        { _.get(profile_data, 'user.github_info.bio', '') }
                    </div>
                    <div class="social-buttons">
                        <a href="{ _.get(profile_data, 'user.github_info.html_url', '') }"
                           show="{ _.get(profile_data, 'user.github_info.html_url', false) }"
                           class="ui circular github plus mini icon button">
                            <i class="github icon"></i>
                        </a>
                    </div>
                    <!--<div show="{GITHUB_INFO_AVAILABLE}" class="languages">
                        <div each="{language in profile.user.languages}" class="ui mini label">
                            {language}
                        </div>
                    </div>-->

                    <!-- <div class="ui large button msg-btn">Message Me</div>
                    <span class="ui icon large button follow-btn"><i class="user icon"></i>Follow</span> -->
                </div>
                <!--Todo get real recent activity-->
                <!--<recent-container></recent-container>-->
            </div>
            <div id="profile-menu" class="ui secondary pointing menu">
                <a class="active item" data-tab="details">
                    Details
                </a>
                <a class="item" data-tab="competitions">
                    Competitions
                </a>
                <a class="item" data-tab="submissions">
                    Submissions
                </a>
                <a class="item" data-tab="datasets">
                    Datasets
                </a>
                <a class="item" data-tab="edit">
                    Account
                </a>
            </div>
        </div>

        <!------------ HOME TAB ----------->
        <div class="ui active details tab" data-tab="details">
            <div class="ui sixteen wide grid container">
                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Competitions</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="stat-breakdown">
                                <table class="stats-table">
                                    <tr>
                                        <td class="category">Competitions Organized:</td>
                                        <td class="statistic">{ _.get(profile_data, 'organized_competitions.length', 0) }
                                        </td>
                                        <!--<td class="category">Organizer Since:</td>
                                        <td class="statistic">02/11/2017</td>-->
                                    </tr>
                                    <!--<tr>
                                        <td class="category">Total Participants:</td>
                                        <td class="statistic">5201</td>
                                        <td class="category">Total Submissions:</td>
                                        <td class="statistic">{ _.get(profile_data, 'solutions', []).length) }</td>
                                    </tr>-->
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <!--<h3>My Featured Competitions</h3>-->
                                <virtual each="{ competition in _.get(profile_data, 'organized_competitions', []) }"
                                         no-reorder>
                                    <competition-tile result="{ competition }" class="item"></competition-tile>
                                </virtual>
                                <p class="no-competitions" style=""
                                   if="{ _.get(profile_data, 'organized_competitions.length', 0) }">No competitions found for this user</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Submissions</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="stat-breakdown">
                                <table class="stats-table">
                                    <tr>
                                        <td class="category">Submissions:</td>
                                        <td class="statistic">{ _.get(profile_data, 'solutions.length', 0) }</td>
                                        <td class="category">User Since:</td>
                                        <!-- TODO: This is probably not the same between profiles/users. Double check -->
                                        <td class="statistic">{ humanize_time( _.get(profile_data, 'user.date_joined', '') ) }
                                        </td>
                                    </tr>
                                    <tr>
                                        <!--<td class="category">Top 10 Finishes:</td>
                                        <td class="statistic">1</td>-->
                                        <td class="category">Competitions Joined:</td>
                                        <td class="statistic">{ _.get(profile_data, 'organized_competitions.length', 0) }
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <h3>Latest Submissions</h3>
                                <submission-tile each="{ _.get(profile_data, 'solutions', []) }"
                                                 class="item"></submission-tile>
                            </div>
                        </div>
                    </div>
                </div>
                <about-me></about-me>
                <div class="flex-content flex-row">
                    <education-container class="education-container"></education-container>
                    <datasets-container class="datasets-container"></datasets-container>
                </div>
                <organization-container class="organization-container"></organization-container>
                <events-container class="events-container"></events-container>
            </div>
        </div>


        <!---------- COMPETITIONS TAB ----------->
        <div class="ui competitions tab" data-tab="competitions">
            <div class="ui sixteen wide grid container">
                <div class="segment-container competitions-summary ui segment sixteen wide">
                    <div class="ui header">
                        Competitions Summary
                    </div>
                    <div class="container-content">
                        <table class="stats-table">
                            <tr>
                                <td class="category">Competitions Organized:</td>
                                <td class="statistic">{ _.get(profile_data, 'organized_competitions.length', 0) }</td>
                                <!--<td class="category">Organizer Since:</td>
                                <td class="statistic">02/11/2017</td>-->
                            </tr>
                            <!--<tr>
                                <td class="category">Total Participants:</td>
                                <td class="statistic">5201</td>
                                <td class="category">Total Submissions:</td>
                                <td class="statistic">73,240</td>
                            </tr>-->
                        </table>
                        <table class="stats-table">
                            <tr>
                                <td class="category">Submissions:</td>
                                <td class="statistic">{ _.get(profile_data, 'solutions.length', 0) }</td>
                                <td class="category">User Since:</td>
                                <td class="statistic">{ humanize_time( _.get(profile_data, 'user.date_joined', '') ) }
                                </td>
                            </tr>
                            <tr>
                                <!--<td class="category">Top 10 Finishes:</td>
                                <td class="statistic">1</td>-->
                                <td class="category">Competitions Joined:</td>
                                <td class="statistic">{_.get(profile_data, 'participating_competitions.length', 0) }
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
            <div class="ui sixteen wide grid container">
                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Competitions I'm Running</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="stat-breakdown">
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <virtual each="{ competition in _.get(profile_data, 'organized_competitions', []) }"
                                         no-reorder>
                                    <competition-tile result="{ competition }" class="item"></competition-tile>
                                </virtual>
                                <p class="no-competitions"
                                   if="{ _.get(profile_data, 'organized_competitions.length', 0) === 0 }">
                                    No competitions found for this user</p>
                            </div>
                            <div class="ui pagination menu">
                                <a class="active item">
                                    1
                                </a>
                                <a class="item">
                                    2
                                </a>
                                <a class="item">
                                    3
                                </a>
                                <a class="item">
                                    4
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Competitions I'm In</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="stat-breakdown">

                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <virtual each="{ competition in _.get(profile_data, 'participating_competitions', []) }"
                                         no-reorder>
                                    <competition-tile result="{ competition }" class="item"></competition-tile>
                                </virtual>
                                <p class="no-competitions"
                                   if="{ _.get(profile_data, 'participating_competitions', []).length == 0 }">
                                    No competitions found for this user</p>
                            </div>
                            <div class="ui pagination menu">
                                <a class="active item">
                                    1
                                </a>
                                <a class="item">
                                    2
                                </a>
                                <a class="item">
                                    3
                                </a>
                                <a class="item">
                                    4
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!---------- SUBMISSIONS TAB ----------->
        <div class="ui submissions tab" data-tab="submissions">
            <submission-tab></submission-tab>
        </div>

        <!------------ DATASETS TAB ----------->
        <div class="ui datasets tab" data-tab="datasets">
            <div class="ui sixteen wide grid container">
                <datasets-table></datasets-table>
            </div>
        </div>

        <!------------ EDIT TAB ----------->
        <div class="ui edit tab" data-tab="edit">
            <div class="ui sixteen wide grid container">
                <div class="ui form">
                    <div class="segment-container social-connect ui segment sixteen wide">
                        <div class="ui header">
                            Connect with Github
                        </div>
                        <div class="container-content">
                            <div class="field">
                                <label>Connect with github</label>
                                <a class="ui large blue button" href="{URLS.SOCIAL_BEGIN.GITHUB}">Login</a>
                            </div>
                            <!--<div class="field" if="{!!profile.github_info}">
                                <label>Connect with github</label>
                                <a class="ui large disabled blue button"
                                   href="/social/login/github">Login</a>
                                <i>You are already connected!</i>
                            </div>-->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!------------ ACCOUNT TAB ----------->
    <div class="ui account tab" data-tab="account">
        <div class="ui grid container">
            <div class="sixteen wide column">
                <form class="ui form">
                    <div class="field">
                        <label>User Name</label>
                        <div class="no-edit">username</div>
                        <div class="field-description">You cannot change your user name. Other Chahub users will
                            not see this name.
                        </div>
                    </div>
                    <hr>
                    <div class="five wide field">
                        <label>Display Name</label>
                        <div class="field-current">
                            <span class="display-name active">displayname</span>
                            <input class="hidden" type="text" name="display-name"
                                   placeholder="displayname"></div>
                        <div class="field-description">This is the name other Chahub users will see.</div>
                    </div>
                    <hr>
                    <div class="five wide field">
                        <label>Email Address</label>
                        <div class="field-current">
                            <span class="email active">email</span>
                            <input class="hidden" type="text" name="email"
                                   placeholder="email">
                        </div>
                    </div>
                    <hr>
                    <div class="five wide field">
                        <label>Email Preferences</label>
                        <div class="ui checkbox">
                            <input type="checkbox" tabindex="0" class="hidden">
                            <label class="email-pref">Subscribe to Email List to receive notifications</label>
                        </div>
                    </div>
                    <hr>
                    <div class="delete">
                        <a href="#">Delete account...</a>
                    </div>
                    <button class="ui button" type="submit">Submit</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.profile_data = {
            user: {},
            github_info: {},
            organized_competitions: [],
            participating_competitions: [],
            solutions: [],
            datasets: [],
            tasks: [],
        }

        self.fields_to_merge = [
            'organized_competitions',
            'datasets',
            'tasks',
            'solutions',
        ]

        self.on('mount', function () {
            particlesJS.load('particles-js', "/static/particles/particles-profile.json", function () {
                console.log('callback - particles.js config loaded');
            })

            if (_.get(self.opts, 'objects')) {
                self.objects = JSON.parse(self.opts.objects)
                self.update()
            }

            $('.secondary.pointing.menu .item').tab({
                onVisible: function () {
                    $('.ui.sticky')
                        .sticky({
                            context: '#submission-container',
                            silent: 'True',
                        })
                        .sticky('refresh')
                },
            });

            $('.ui.checkbox').checkbox();
            self.update_profiles();
        })

        self._profile_data_update = function (data) {
            if (_.get(data, 'participants', false)) {
                data.participants.forEach(function (participant) {
                    self.profile_data.participating_competitions.push(participant.competition)
                })
            }

            self.fields_to_merge.forEach(function (field) {
                self.profile_data[field] = _.merge(self.profile_data[field], data[field])
            })
        }

        self._user_profile_data_update = function (data) {
            data.profiles.forEach(function( profile ) {
                self._profile_data_update(profile)
            })
        }

        self.update_profiles = function () {
            if (self.opts.mode === 'user') {
                CHAHUB.api.get_user(self.opts.objects)
                    .done(function (data) {
                        self.profile_data.user = data
                        if (_.get(data, 'github_info', false)) {
                            self.profile_data.github_info = data.github_info
                        }
                        self._user_profile_data_update(data)
                        self.update()
                        CHAHUB.events.trigger("profile_loaded", self.profile_data)
                    })
                    .fail(function (response) {
                        toastr.error("Failed to retrieve profile: " + self.opts.objects[0])
                    })
            } else {
                self.objects = _.isArray(self.objects) ? self.objects : [self.objects]
                CHAHUB.api.get_profiles(self.objects)
                    .done(function (data) {
                        data.forEach(function (profile) {
                            if (_.get(profile, 'user', false) && _.isEmpty(self.profile_data.user))
                            {
                                self.profile_data.user = profile.user
                                if (_.get(profile.user, 'github_info', false) && _.isEmpty(self.profile_data.github_info)) {
                                        self.profile_data.github_info = profile.user.github_info
                                }
                            }
                            self._profile_data_update(profile)
                        })
                        self.update()
                        CHAHUB.events.trigger("profile_loaded", self.profile_data)
                    })
                    .fail(function (response) {
                        toastr.error("Failed to retrieve profile")
                    })
            }
        }

        self.prepare_results = function () {
            self.sorted_competitions.forEach(function (comp_result) {
                var humanized_time = humanize_time(comp_result.current_phase_deadline)
                comp_result.alert_icon = humanized_time < 0;
                comp_result._obj_type = 'competition';
                if (comp_result.alert_icon) {
                    comp_result.pretty_deadline_time = 'Phase ended ' + Math.abs(humanized_time) + ' days ago'
                } else {
                    comp_result.pretty_deadline_time = humanized_time
                }
            })
        }
    </script>

    <style>
        .circular.github.button {
            background-color: #582c80;
            color: white;
        }

        .details {
            margin: 0 -1em
        }

        .competitions.tab .primary-container,
        .edit.tab .primary-container,
        about-me,
        events-container,
        organization-container {
            width: 100% !important;
        }

        education-container {
            width: 35% !important
        }

        datasets-container {
            width: 62% !important
        }

        recent-container {
            margin: 1em 1em 1em auto;
            text-align: right;
            float: right
        }

        .details > .container {
            margin-top: 1em
        }

        #editor-container {
            height: auto
        }

        .stats-table {
            width: 100%;
            border-bottom: 1px solid #dcdcdc;
            padding-bottom: 1em;
            margin-bottom: 1em
        }

        .stats-table .category {
            font-weight: 600;
            font-size: 1.15em;
            color: #2b2b2b;
            text-align: left;
            padding: 0 10px
        }

        .stats-table .statistic {
            font-size: .85em;
            color: #a0a0a0;
            text-align: right
        }

        .competitions > .container > .ui.segment,
        .details > .container > .ui.segment {
            width: 47.5%;
            margin: 1em;
            padding: 0
        }

        .competitions.tab .container-content,
        .edit.tab .container-content {
            margin: 10px
        }

        #profile-menu {
            margin: 0
        }

        .competition-segment > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #f2faff;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px #dcdcdc
        }

        .competition-segment {
            margin: 15px 0
        }

        .bio-segment {
            width: 100% !important
        }

        .biography {
            padding: 1.55em;
            color: #a0a0a0
        }

        .no-margin {
            margin: 0 !important
        }

        .flex-content {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            flex-wrap: wrap;
            margin: 1em 0
        }

        .competition-segment .flex-content {
            flex-direction: column;
            margin: 0;
            padding: 1em !important
        }

        .list-tile > a {
            font-size: 15px;
            font-weight: 600
        }

        .date-complete {
            color: #a0a0a0;
            font-size: .8em
        }

        .competitions.tab, .edit.tab .sixteen.wide.grid.container {
            margin: 2em -1em
        }

        .competitions.tab .pagination.menu {
            margin: 1.25em .5em .25em
        }

        .edit .segment-container {
            padding: 0 !important;
            height: 100%;
            text-align: left;
            margin: 0 -1em !important
        }

        .competitions .segment-container {
            padding: 0 !important;
            width: 100%
        }

        .competitions.tab .segment-container > .header,
        .datasets.tab .segment-container > .header,
        .edit.tab .segment-container > .header {
            font-size: 1em !important;
            text-align: left !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #f2faff;
            padding: 10px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px #dcdcdc
        }

        .competitions.tab .list-tile,
        .edit.tab .list-tile {
            font-size: .75em
        }

        .competitions.tab .list-tile a,
        .edit.tab .list-tile a {
            font-size: 10px
        }

        .competitions-summary {
            width: 100% !important;
            margin: 1em !important
        }

        .competitions.tab .stats-table {
            display: inline-flex;
            justify-content: space-between;
            margin: 1em 4em 1em 1em;
            width: auto;
            border-bottom: none
        }

        .competitions-summary .container-content {
            text-align: center
        }

        .datasets.tab datasets-table {
            width: 100%;
            min-width: 50% !important;
            padding: 0 !important;
            margin: 3em auto !important;
        }

        .delete-button {
            color: #c23100 !important;
            text-align: center;
            cursor: pointer;
            text-transform: capitalize;
        }

        .delete-button:hover {
            color: #cc1c1c !important;
            text-decoration: underline;
        }

        .datasets-segment {
            margin-top: 3em !important;
            width: 100%;
            padding: 0 !important
        }

        .datasets-segment .container-content {
            padding: 1em
        }

        .submissions.tab {
            margin-top: 2em;
        }

        .no-competitions {
            border-top: 1px solid gainsboro;
            color: #909090;
            padding-top: 1em;
        }

    </style>
</profile-page>

<about-me id="about-me">
    <div class="bio-segment primary-segment ui segment sixteen wide">
        <div class="ui header">
            About Me
        </div>
        <div class="list-tile">
            <div class="biography">
                <div id="bio">
                    { _.get(profile_data, 'github_info.bio', 'No information found') }
                </div>
                <div id="editor-container">
                    <textarea id="editor"></textarea>
                </div>
            </div>
        </div>
    </div>

    <script>
        var self = this
        CHAHUB.events.on('profile_loaded', function (profile_data) {
            self.profile_data = profile_data
            self.update()

            $('#editor-container').hide()
            //document.getElementById('bio').innerHTML = profile.github_info.bio
        })
    </script>

    <style>

        .primary-segment > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px 10px 10px 1.75em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .primary-segment {
            margin: 1em 0 !important;
            width: 100% !important;
            padding: 0 !important;
        }

        .biography {
            padding: 30px;
            color: #A0A0A0;
        }

        .flex-content {
            display: flex;
            flex-direction: row;
        }

        #editor-container {
            padding-top: 2em;
        }

    </style>
</about-me>

<education-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Education
            <!--
            <div class="right floated ui button edit-button" onclick="{edit_education}"
                 if="{!edit_edu}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_education}"
                 if="{!edit_edu}">Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_education}"
                 if="{!!edit_edu}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_education}"
                 if="{!!edit_edu}">
                Cancel
            </div>
            -->
        </div>
        <div class="container-content">
            <education-tile></education-tile>
        </div>
    </div>

    <style>
        .primary-container {
            width: 100%;
        }

        .segment-container {
            padding: 0 !important;
            height: 100%;
            min-width: 290px;
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .container-content {
            margin: 20px;
        }

        .name {
            font-size: 1.2em;
            font-weight: 600;
            line-height: 1.2em;
        }

        .degree {
            font-size: 1.16em;
            font-weight: 200;
        }

        .attended {
            color: #909090;
            margin: 5px 0;
        }

        .awards {
            color: #909090;
        }

    </style>
</education-container>

<education-tile>
    <div class="no-education">No information found</div>

    <style>
        .no-education {
            color: #909090;
        }
    </style>
</education-tile>

<datasets-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Latest Datasets
        </div>
        <div class="container-content">
            <datasets-table></datasets-table>
        </div>
    </div>

    <style>

        .segment-container {
            padding: 0 !important;
            height: 100%;
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .container-content {
            margin: 20px;
        }

        .name {
            font-size: 1.2em;
            font-weight: 600;
            line-height: 1.2em;
        }

        .degree {
            font-size: 1.16em;
            font-weight: 200;
        }

        .attended {
            color: #909090;
            margin: 5px 0;
        }

        .awards {
            color: #909090;
        }

    </style>
</datasets-container>

<datasets-table>
    <table class="ui celled table">
        <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Uploaded</th>
            <!-- Bring back later for publishing and deleting datasets
            <th class="center aligned column">Public</th>
            <th class="center aligned column">Delete</th> -->
        </tr>
        </thead>
        <tbody>
        <tr each="{_.get(profile_data, 'datasets', [])}">
            <td data-label="Name"><a href="#"><i class="download icon"></i>{name}</a></td>
            <td data-label="Type">{type}</td>
            <td data-label="Uploaded">{upload_date}</td>

            <!-- Bring back later for publishing, deleting, and adding new datasets
            <td data-label="Public" class="center aligned column">
                <div class="ui icon button public-button {green: published}"
                     onclick="{publish}"><i class="file icon"></i>
                </div>
            </td>
            <td data-label="Delete" class="center aligned column">
                <a class="delete-button" href="#" onclick="{delete_dataset}">Delete</a>
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <input type="file" id="dataset-upload" style="display:none"/>
                <a href="#" onclick="{upload_dataset}"><i class="plus icon"></i>Add new dataset</a>
            </td>-->
        </tr>
        <tr if="{!datasets}">
            <td colspan="3" class="empty-datasets">No datasets found</td>
        </tr>
        </tbody>
    </table>

    <script>
        var self = this
        CHAHUB.events.on('profile_loaded', function (profile_data) {
            self.profile_data = profile_data
            self.update()
        })

    </script>

    <style>
        .empty-datasets {
            color: #909090;
        }
    </style>
</datasets-table>

<organization-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Organizations
            <!--
            <div class="right floated ui button edit-button" onclick="{edit_organization}"
                 if="{!edit_organization}">
                Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_organization}"
                 if="{!edit_organization}">
                Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_organization}"
                 if="{!!edit_organization}">
                Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_organization}"
                 if="{!!edit_organization}">
                Cancel
            </div>
            -->
        </div>
        <div class="container-content">
            No information found
        </div>
    </div>

    <style>
        .segment-container {
            padding: 0 !important;
            margin: 1em 0 !important;
            height: auto
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #f2faff;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px #dcdcdc
        }

        .container-content {
            margin: 20px;
            color: #909090;
        }

        .name {
            font-size: 1.2em;
            font-weight: 600;
            line-height: 1.2em
        }

        .degree {
            font-size: 1.16em;
            font-weight: 200
        }

        .attended {
            margin: 5px 0
        }

        .attended, .awards {
            color: #909090
        }

    </style>
</organization-container>

<organization-tile>
    <img class="ui middle aligned tiny image" src="https://via.placeholder.com/150">
    <div class="org-container first">
        <div class="name">Placeholder Organization</div>
        <div class="type">Placehold</div>
        <div class="description">Set out to placehold all of the organizations for this description
        </div>
    </div>
    <div class="ui divider"></div>
</organization-tile>

<events-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            Events and Meetups
            <!--
            <div class="right floated ui button edit-button" onclick="{edit_events}"
                 if="{!edit_events}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_events}"
                 if="{!edit_events}">Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_events}"
                 if="{!!edit_events}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_events}"
                 if="{!!edit_events}">Cancel
            </div>
            -->
        </div>
        <div class="container-content">
            No information found
        </div>
    </div>

    <style>

        .segment-container {
            padding: 0 !important;
            margin: 1em 0 !important;
            height: auto;
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .container-content {
            margin: 20px;
            color: #909090;
        }

        .name {
            font-size: 1.2em;
            font-weight: 600;
            line-height: 1.2em;
        }

        .date {
            color: rgba(0, 0, 0, .6);
            margin: 5px 0;
        }

        .brief {
            color: rgba(0, 0, 0, .6);
        }

        .website {
            padding: 10px 0;
        }

    </style>
</events-container>

<events-tile>
    <div class="name">Seattle Machine Learning Meetup</div>
    <div class="date">Every Wednesday</div>
    <div class="brief">We meet every Wednesday to discuss Machine Learning Protocols and the science
        behind them. All skill levels welcome to join!
    </div>
    <div class="website"><a href="#">Facebook Link</a></div>
    <div class="ui divider"></div>
</events-tile>

<recent-container>
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            Recent Activity
        </div>
        <div class="container-content">
            <!--TODO get real data-->
            <div class="list-activity">
                <div class="list-tile">
                    <a href="#">Competition: Finding relevant data on ice floes</a>
                    <div class="date-complete">Competition ended 03/01/2018</div>
                </div>
                <div class="list-tile">
                    <a href="#">Submission: Pathfinding in the dark</a>
                    <div class="date-complete">Submitted 03/01/2018</div>
                </div>
                <div class="list-tile">
                    <a href="#">Dataset: Handwriting</a>
                    <div class="date-complete">Submitted 03/01/2018</div>
                </div>
            </div>
        </div>
    </div>

    <style>
        .primary-container {
            width: 100%;
        }

        .segment-container {
            padding: 0 !important;
            height: 100%;
            text-align: left;
        }

        .segment-container > .header {
            font-size: 1em !important;
            text-align: left !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .container-content {
            margin: 10px;
        }

        .list-tile {
            font-size: 0.75em;
        }

        .list-tile a {
            font-size: 10px;
        }

    </style>
</recent-container>

<submission-tab>
    <div class="ui sixteen wide grid container">
        <div id="submission-container" class="segment-container ui segment sixteen wide">
            <div class="ui header">
                My Submissions
            </div>
            <div class="container-content">
                <div class="ui middle aligned unstackable compact divided link items content-desktop">
                    <submission-tile each="{ _.get(profile_data, 'solutions', []) }" class="item"></submission-tile>
                    <p if="{ _.get(profile_data, 'solutions.length', 0) === 0 }">No submissions found for this user</p>
                </div>
            </div>
        </div>
        <!-- <div class="segment-container data-container ui sticky segment sixteen wide">
            <div class="ui header">
                Submission Data
            </div>
            <div class="container-content" if={!selected_submission}>
                <i>Please select a submission from the left side to view data about it.</i>
            </div>
            <div class="container-content" if={selected_submission}>
                Competition Link:<a href="{ selected_submission.url }">{ selected_submission.url }</a>
            </div>
        </div> -->
    </div>

    <script>
        var self = this

        CHAHUB.events.on('profile_loaded', function (profile_data) {
            self.profile_data = profile_data
            self.update()
        })
    </script>

    <style>
        :scope {
            display: block;
        }

        .sixteen.wide.grid {
            padding-top: 1em;
        }

        .segment-container {
            padding: 0 !important;
            height: 100%;
            width: 100%;
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px 10px 10px 1.25em;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .container-content {
            margin: 10px;
            display: flex;
            flex-direction: column;
            flex: 1 0 auto;
            overflow-x: auto;
        }
    </style>
</submission-tab>

<submission-tile>
    <div class="ui tiny image">
        <img src="{logo || URLS.STATIC('img/img-wireframe.png') }" class="ui avatar image">
    </div>
    <div class="content">
        <div class="header">
            {title}
        </div>
        <div class="description">
            <p>{description}</p>
        </div>
        <div class="extra">
            <div class="mobile_linewrap">
                <span class="url"><a href="{url}">{url}</a></span>
            </div>
        </div>
    </div>
    <div class="sub-btn-container">
        <a href="{url}">
            <button class="ui teal icon button sub-btn"><i class="external alternate icon"></i> Competition</button>
        </a>
        <button class="ui blue icon button sub-btn"><i class="download icon"></i> Submission</button>
    </div>

    <style type="text/stylus">
        :scope
            display block

        .tiny.image
            width 4em !important

        .header
            font-size 1.25em !important

        .description
            color #909090 !important
            font-size 0.9em !important
            margin-top 0 !important

        .extra
            font-size 0.9em !important

        .sub-btn-container
            text-align right
            width 125px

        .sub-btn
            margin 5px !important
            width 121px
    </style>
</submission-tile>
