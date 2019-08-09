<profile-page-user>
    <div id="particles-js">
        <a href="/"><img id="brand_logo" src="{URLS.STATIC('img/temp_chahub_logo_beta.png')}"></a>
    </div>

    <div class="ui container">
        <div class="ui profile-segment segment">
            <div class="ui container profile-header">
                <div class="holder">
                    <img class="profile-img" src="{_.get(_.get(profile, 'github_info', {}), 'avatar_url', URLS.STATIC('img/img-wireframe.png'))}" alt="placeholder">
                </div>
                <div class="profile-user">
                    {_.get(profile, 'username', 'anonymous / N/A')}
                    <div class="profile-brief">
                        <div class="location">{_.get(_.get(profile, 'github_info', {}), 'location', '')}</div>
                        <div class="occupation">{_.get(_.get(profile, 'github_info', {}), 'company', '')}</div>
                        {_.get(_.get(profile, 'github_info', {}), 'bio', '')}
                    </div>
                    <div class="social-buttons">
                        <a href="{_.get(_.get(profile, 'github_info', {}), 'html_url', '')}" if="{_.get(_.get(profile, 'github_info', {}), 'html_url', false)}"
                           style="background-color: #582c80; color: white;"
                           class="ui circular github plus mini icon button">
                            <i class="github icon"></i>
                        </a>
                    </div>
                    <!--<div class="languages">
                        <div each="{language in profile.languages}" class="ui mini label">
                            {language}
                        </div>
                    </div>-->

                    <!-- <div class="ui large button msg-btn">Message Me</div>
                    <span class="ui icon large button follow-btn"><i class="user icon"></i>Follow</span> -->
                </div>
                <recent-container-user></recent-container-user>
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
                <a if="{window.IS_OWN_PROFILE}" class="item" data-tab="edit">
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
                                        <td class="statistic">{profile.organized_competitions.length | 0}</td>
                                        <td class="category">Organizer Since:</td>
                                        <td class="statistic"></td>
                                    </tr>
                                    <tr>
                                        <td class="category">Total Participants:</td>
                                        <td class="statistic">{profile.organized_competitions.participant_count | 0}
                                        </td>
                                        <td class="category">Total Submissions:</td>
                                        <td class="statistic">{profile.organized_competitions.submission_count | 0}</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <h3>My Featured Competitions</h3>
                                <!--<competition-tile-user each="{ profile.organized_competitions.slice(0,5) }" no-reorder class="item"></competition-tile-user>-->
                                <competition-tile-user each="{ _.get(profile, 'organized_competitions', []).slice(0,5) }" no-reorder class="item"></competition-tile-user>
                                <p class="no-competitions" style="" if="{ _.get(profile, 'organized_competitions', []).length === 0 }">
                                    No competitions found for this user</p>
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
                                        <td class="statistic">{profile.created_solutions.length | 0}</td>
                                        <td class="category">User Since:</td>
                                        <td class="statistic"></td>
                                    </tr>
                                    <tr>
                                        <td class="category">Competitions Joined:</td>
                                        <td class="statistic">{profile.organized_competitions.length}</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <h3>Latest Submissions</h3>
                                <submission-tile-user each="{ _.get(profile, 'created_solutions', []) }" class="item"></submission-tile-user>
                                <p class="no-competitions" style="" if="{ _.get(profile, 'created_solutions', []).length === 0 }">
                                    No solutions found for this user</p>
                            </div>
                        </div>
                    </div>
                </div>
                <about-me-user opts={profile}></about-me-user>
                <div class="flex-content flex-row">
                    <education-container-user class="education-container"></education-container-user>
                    <datasets-container-user class="datasets-container"></datasets-container-user>
                </div>
                <organization-container-user class="organization-container"></organization-container-user>
                <events-container-user class="events-container"></events-container-user>
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
                                <td class="statistic">{_.get(profile, 'organized_competitions', []).length}</td>
                                <!--<td class="category">Organizer Since:</td>
                                <td class="statistic">02/11/2017</td>-->
                            </tr>
                            <tr>
                                <!--<td class="category">Total Participants:</td>
                                <td class="statistic">5201</td>-->
                                <td class="category">Total Submissions:</td>
                                <td class="statistic">{_.get(profile, 'created_solutions', []).length}</td>
                            </tr>
                        </table>
                        <table class="stats-table">
                            <tr>
                                <td class="category">Submissions:</td>
                                <td class="statistic">{_.get(profile, 'created_solutions', []).length}</td>
                                <td class="category">User Since:</td>
                                <td class="statistic">{pretty_date(profile.date_joined)}</td>
                            </tr>
                            <tr>
                                <td class="category">Top 10 Finishes:</td>
                                <td class="statistic">1</td>
                                <td class="category">Competitions Joined:</td>
                                <td class="statistic">{participants.length }</td>
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
                                <competition-tile-user each="{ profile.organized_competitions }" no-reorder
                                                       class="item"></competition-tile-user>
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
                                <virtual if="{ _.get(profile_data, 'participating_competitions', false) }"
                                         each="{ competition in _.get(profile_data, 'participating_competitions', []) }"
                                         no-reorder>
                                    <competition-tile result="{competition}" class="item"></competition-tile>
                                </virtual>
                                <p class="no-competitions"
                                   if="{ _.get(profile_data, 'participating_competitions', false) } || _.get(profile_data, 'participating_competitions', []).length === 0">
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
            <submission-tab-user></submission-tab-user>
        </div>

        <!------------ DATASETS TAB ----------->
        <div class="ui datasets tab" data-tab="datasets">
            <div class="ui sixteen wide grid container">
                <datasets-table-user-tab></datasets-table-user-tab>
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
                            <div class="field" if="{!profile.github_info}">
                                <label>Connect with github</label>
                                <a class="ui large blue button" href="/social/login/github">Login</a>
                            </div>
                            <div class="field" if="{!!profile.github_info}">
                                <label>Connect with github</label>
                                <a class="ui large disabled blue button"
                                   href="/social/login/github">Login</a>
                                <i>You are already connected!</i>
                            </div>
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
                            not
                            see this name.
                        </div>
                    </div>
                    <hr>
                    <div class="five wide field">
                        <label>Display Name</label>
                        <div class="field-current">
                            <span onclick="editfield(event)" class="display-name active">displayname</span>
                            <input class="hidden" type="text" name="display-name"
                                   placeholder="displayname"></div>
                        <div class="field-description">This is the name other Chahub users will see.</div>
                    </div>
                    <hr>
                    <div class="five wide field">
                        <label>Email Address</label>
                        <div class="field-current">
                            <span onclick="editfield(event)" class="email active">email</span>
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
        self.profile = {
            github_info: {
                avatar_url: '',
                bio: ''
            },
            username: '',
            name: '',
            email: '',
            bio: '',
            organized_competitions: []
        }
        self.organized_competitions = []

        self.profile_data = {
            participants: [],
            participating_competitions: []
        }

        self.participating_competitions = []
        self.datasets = []
        self.submissions = []
        self.sorted_competitions = []
        self.participants = []

        self.on('mount', function () {
            particlesJS.load('particles-js', "/static/particles/particles-profile.json", function () {
                console.log('callback - particles.js config loaded');
            })

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
            //self.update_information();
            self.update_user();
        })

        self.update_user = function () {
            CHAHUB.api.get_user(PROFILE_OBJECTS)
                .done(function (data) {
                    console.log(data)
                    self.profile = data
                    data.profiles.forEach(function (profile) {
                        profile.participants.forEach(function (participant) {
                            self.profile_data.participants.push(participant)
                        })
                    })
                    self.profile_data.participants.forEach(function (participant) {
                        self.profile_data.participating_competitions.push(participant.competition)
                    })
                    self.update()
                    CHAHUB.events.trigger("profile_loaded")
                })
                .fail(function (response) {
                    toastr.error("Unable to fetch user")
                })
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

        self.submissions = [
            {
                logo: 'http://placeimg.com/206/206/any',
                _obj_type: 'competition',
                title: 'Find Stuff in Data',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '10',
                prize: '1200',
            },
            {
                logo: 'http://placeimg.com/207/207/any',
                _obj_type: 'competition',
                title: 'Chance of a Car Running into a Tree',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '1090',
                prize: '2400',
            },
            {
                logo: 'http://placeimg.com/208/208/any',
                _obj_type: 'competition',
                title: 'Trading bot',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '190',
                prize: '65400',
            }
        ]

        self.publish = function (event) {
            var txt;

            if (event.item.published) {
                var r = confirm("Are you sure you want to make this dataset private?");
                if (r === true) {
                    txt = "This dataset is now private";
                    return event.item.published = false;
                } else {
                    txt = "This dataset is still public";
                    return event.item.published = true;
                }
            } else {
                var r = confirm("Are you sure you want to publish this dataset?");
                if (r === true) {
                    txt = "This dataset is now public!";
                    return event.item.published = true;
                } else {
                    txt = "This dataset is still private";
                    return event.item.published = false;
                }

            }
        }

        self.delete_dataset = function (event) {
            var txt;

            var r = confirm("Are you sure you want to delete this dataset?");
            if (r === true) {
                txt = "This dataset has been deleted!";
                // TODO: Delete this item from the model
            } else {
                txt = "This dataset is still public";
            }
            event.preventDefault();
        }

        self.upload_dataset = function (event) {
            $('#dataset-upload').trigger('click');
            event.preventDefault();
            // TODO: Needs modal for Name, Type, and Public
        }

    </script>

    <style>
        .details {
            margin: 0 -1em
        }

        .competitions.tab .primary-container,
        .edit.tab .primary-container,
        about-me,
        events-container,
        organization-container {
            width: 100%
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
            width: auto;
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
</profile-page-user>

<about-me-user id="about-me">
    <div class="bio-segment primary-segment ui segment sixteen wide">
        <div class="ui header">
            About Me
        </div>
        <div class="list-tile">
            <div class="biography">
                <!--<div id="bio" if={!!profile.github_info.bio}>{profile.github_info.bio}</div>-->
                <div id="bio" if={!!profile.github_info.bio}>{_.get(_.get(profile, 'github_info', {}), '')}</div>
                <div id="bio" if={!profile.github_info.bio}>No information found</div>
            </div>
        </div>
    </div>

    <script>
        var self = this
        self.profile = {
            github_info: {
                avatar_url: '',
                bio: ''
            },
            username: '',
            name: '',
            email: '',
            bio: '',
            organized_competitions: []
        }

        CHAHUB.events.on('profile_loaded', function () {

            self.update({profile: self.parent.profile})
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
</about-me-user>

<education-container-user class="primary-container">
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
            <education-tile-user></education-tile-user>
        </div>
    </div>

    <script>

        self.edit_education = function () {
            $('#bio', self.root)
            self.edit_education = true
            self.simplemde.value(self.user.bio_markdown);
            $('#editor-container').attr('style', 'display: block !important')
            self.simplemde.codemirror.refresh();
        }

        self.add_education = function () {
            self.edit_education = true
        }

        self.save_education = function () {
            self.edit_education = false
            self.user.bio_markdown = self.simplemde.value()
            self.user.bio = marked(self.simplemde.value())
            $('#editor-container').attr('style', 'display: none !important')
            document.getElementById('bio').innerHTML = self.user.bio
        }

        self.cancel_edit = function () {
            self.edit_education = false
            $('#editor-container').attr('style', 'display: none !important')
        }
    </script>

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
</education-container-user>

<education-tile-user>
    <div class="no-education">No information found</div>

    <style>
        .no-education {
            color: #909090;
        }
    </style>
</education-tile-user>

<datasets-container-user class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Latest Datasets
        </div>
        <div class="container-content">
            <datasets-table-user></datasets-table-user>
        </div>
    </div>

    <script>
        var self = this

        CHAHUB.events.on('profile_loaded', function () {
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            console.log(self.parent.profile)
            self.update({profile: self.parent.profile})
        })
    </script>

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
</datasets-container-user>

<datasets-table-user>
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
        <tr each="{datasets_slice}">
            <td data-label="Name"><a href="#"><i class="download icon"></i>{name}</a></td>
            <td data-label="Type">{type}</td>
            <td data-label="Uploaded">{created_when}</td>

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
        </tbody>
    </table>

    <script>
        var self = this

        CHAHUB.events.on('profile_loaded', function () {
            self.update({
                datasets_slice: self.parent.profile.created_datasets.slice(0, 5),
            })
        })
    </script>
</datasets-table-user>

<datasets-table-user-tab>
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
        <tr each="{datasets}">
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
        </tbody>
    </table>

    <script>
        var self = this

        CHAHUB.events.on('profile_loaded', function () {
            console.log(self.parent.profile)
            self.update({
                datasets: self.parent.profile.created_datasets,
            })
        })
    </script>
</datasets-table-user-tab>

<organization-container-user class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Organizations
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
</organization-container-user>

<organization-tile-user>
    <img class="ui middle aligned tiny image" src="https://via.placeholder.com/150">
    <div class="org-container first">
        <div class="name">Placeholder Organization</div>
        <div class="type">Placehold</div>
        <div class="description">Set out to placehold all of the organizations for this description
        </div>
    </div>
    <div class="ui divider"></div>
</organization-tile-user>

<events-container-user class="primary-container">
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
</events-container-user>

<events-tile-user>
    <div class="name">Seattle Machine Learning Meetup</div>
    <div class="date">Every Wednesday</div>
    <div class="brief">We meet every Wednesday to discuss Machine Learning Protocols and the science
        behind them. All skill levels welcome to join!
    </div>
    <div class="website"><a href="#">Facebook Link</a></div>
    <div class="ui divider"></div>
</events-tile-user>

<recent-containe-user>
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            Recent Activity
        </div>
        <div class="container-content">
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
</recent-containe-user>

<submission-tab-user>
    <div class="ui sixteen wide grid container">
        <div id="submission-container" class="segment-container ui segment sixteen wide">
            <div class="ui header">
                My Submissions
            </div>
            <div class="container-content">
                <div class="ui middle aligned unstackable compact divided link items content-desktop">
                    <submission-tile each="{_.get(profile, 'created_solutions', [])}" onclick="{show_table}"
                                     class="item"></submission-tile>
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

        self.submissions = [
            {
                logo: 'http://placeimg.com/200/200/any',
                _obj_type: 'competition',
                title: 'Find Stuff in Data',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '10',
                prize: '1200',
            },
            {
                logo: 'http://placeimg.com/201/201/any',
                _obj_type: 'competition',
                title: 'Chance of a Car Running into a Tree',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '1090',
                prize: '2400',
            },
            {
                logo: 'http://placeimg.com/202/202/any',
                _obj_type: 'competition',
                title: 'Trading bot',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '190',
                prize: '65400',
            },
        ]

        CHAHUB.events.on('profile_loaded', function () {
            self.update({profile: self.parent.profile})
        })
    </script>

    <style type="text/stylus">
        :scope
            display block

        .sixteen.wide.grid
            padding-top: 1em;

        .segment-container {
            padding: 0 !important;
            height: 100%;
            width: 100%;
        }

        #submission-container {
            margin: 0 150px;
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
</submission-tab-user>

<submission-tile-user>
    <div class="ui tiny image">
        <img src="{logo || 'http://placeimg.com/203/203/any' }" class="ui avatar image">
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
</submission-tile-user>

<competition-tile-user onclick="{redirect_to_url}">
    <div class="floating-actions { is-admin: USER_IS_SUPERUSER }">
        <i class="icon green pencil alternate"
           onclick="{ edit_competition }"></i>
        <i class="icon red delete" onclick="{ delete_competition }"></i>
        <i class="icon { yellow: locked, unlock: locked, lock: !locked }" onclick="{ lock_competition}"></i>
    </div>
    <div class="ui tiny image">
        <img src="{logo || URLS.STATIC('img/img-wireframe.png')}" class="ui avatar image">
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
                <span class="url"><a href="{url}">{url_short(url)}</a></span>
                <span class="date">
                {pretty_date(start)}
                <virtual if="{end}">
                    - {pretty_date(end)}
                </virtual>
            </span>
                <div class="mobile_labelwrap"></div>
                <span class="participant_label ui right floated mini label tooltip" data-content="Participant count">
                    <i class="user icon"></i> {participant_count}
                </span>
                <span class="deadline_label ui right floated mini label tooltip {red: !alert_icon}"
                      data-content="Deadline of the current phase"
                      show="{current_phase_deadline}">
                    <i show="{!alert_icon}" class="alarm icon"></i> {pretty_deadline_time}
                </span>
                <span class="deadline_label ui right floated mini label" show="{!current_phase_deadline}">
                    Never ends
                </span>
                <span class="prize_label ui right floated mini label tooltip" data-content="Prize Amount"
                      show="{prize}">
                    <i class="yellow trophy icon"></i> {prize}
                </span>
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.on("mount", function () {
            $(".tooltip", self.root).popup()
            $(self.refs.modal).modal()
        })

        self.redirect_to_url = function () {
            window.open(self.url, '_blank');
        }

        self.url_short = function (url) {
            return url.replace(/^(?:https?:\/\/)?(?:www\.)?/i, "").split('/')[0];
        }

        self.edit_competition = function (event) {
            CHAHUB.events.trigger('competition_selected', event.item)
            event.cancelBubble = true
        }

        self.delete_competition = function (event) {
            // TODO - Need to delete the competition on confirm, else do nothing.
            if (confirm(`Are you sure you want to delete "${event.item.title}?"`)) {
                alert('Deleted')
            }
            event.cancelBubble = true
        }

        self.lock_competition = function (event) {
            // TODO - Need to lock the competition and change icon/color to represent locked and unlocked state
            event.cancelBubble = true
        }
    </script>

    <style type="text/stylus">
        :scope
            display block
            position relative

        :scope:hover .floating-actions.is-admin
            opacity 1

        .floating-actions
            position absolute
            top 0
            right 0
            opacity 0
            z-index 10

        .content
            .description
                margin-top 0 !important
                color #808080 !important
                display block
                font-size .9em !important

            p
                line-height 1.1em !important

            @media screen and (max-width 645px)
                padding-left 0.8em !important

        .extra
            margin-top 0
            @media screen and (max-width 749px)
                margin-bottom 0 !important

            .url
                font-size .8em
                color rgba(0, 0, 255, 0.6) !important
                white-space nowrap
                overflow hidden
                text-overflow ellipsis
                max-width 90vw
                display block !important
                @media screen and (min-width 2560px)
                    margin-bottom: 10px;
                    overflow: visible;
                @media screen and (max-width 750px) {
                    margin-bottom: -6px;
                }

            .date
                font-size 0.8em
                color #8c8c8c !important

        .ui.avatar.image
            max-width 4em
            @media screen and (max-width 750px)
                max-width 3em
            @media screen and (min-width 2560px)
                max-width 8em

        .ui.image
            max-width 60px
            display inline-grid !important
            justify-content center
            @media screen and (min-width 2560px)
                max-width 240px

        .participant_label
            background-color #475e6f !important
            border-color #475e6f !important
            color #dfe3e5 !important
            right 0
            margin 0 2px !important
            text-align right

            .icon
                float left

        .prize_label
            background-color rgba(99, 84, 14, 0.68) !important
            border-color rgba(99, 84, 14, 0.68) !important
            color #dee2e4 !important
            margin 0 2px !important

        .deadline_label
            margin 0 2px !important

        .mobile_linewrap
            white-space nowrap
            overflow hidden
            text-overflow ellipsis
            color rgba(0, 0, 255, 0.6)
            margin-bottom 5px !important
            margin-right 0 !important

        .label
            @media screen and (min-width 2560px)
                font-size 1.2rem !important

        .mobile_labelwrap
            display block
            @media screen and (min-width 500px)
                display inline-block

        @media screen and (min-width 2560px)
            *
                font-size 1.5rem !important

            .header
                font-size 2rem !important

    </style>
</competition-tile-user>
