<profile-page>
    <div id="particles-js">
        <a href="/"><img id="brand_logo" src="{URLS.STATIC('img/temp_chahub_logo_beta.png')}"></a>
    </div>

    <div class="ui container">
        <div class="ui profile-segment segment">
            <div class="ui container profile-header">
                <div class="holder">
                    <img class="profile-img" src="http://i.pravatar.cc/120" alt="placeholder">
                    <div class="social-buttons">
                        <button class="ui circular facebook mini icon button">
                            <i class="facebook icon"></i>
                        </button>
                        <button class="ui circular twitter mini icon button">
                            <i class="twitter icon"></i>
                        </button>
                        <button class="ui circular linkedin mini icon button">
                            <i class="linkedin icon"></i>
                        </button>
                        <button style="background-color: #582c80; color: white;"
                                class="ui circular github plus mini icon button">
                            <i class="github icon"></i>
                        </button>
                    </div>
                </div>
                <div class="profile-user">
                    Profile Name
                    <div class="profile-brief">
                        <div class="location">Seattle, Washington USA</div>
                        <div class="occupation">Programmer at MadeUp Company</div>
                        A brief description of the user goes here
                    </div>
                    <div class="languages">
                        <div class="ui mini label">
                            Python
                        </div>
                        <div class="ui mini label">
                            C++
                        </div>
                        <div class="ui mini label">
                            Go
                        </div>
                    </div>
                    <!-- <div class="ui large button msg-btn">Message Me</div>
                    <span class="ui icon large button follow-btn"><i class="user icon"></i>Follow</span> -->
                </div>
                <recent-container></recent-container>
            </div>
            <div id="profile-menu" class="ui secondary pointing menu">
                <a class="active item" data-tab="details">
                    Details
                </a>
                <a class="item" data-tab="competitions">
                    Competitions
                </a>
                <a class="item" data-tab="datasets">
                    Datasets
                </a>
                <a class="item" if="{USER_AUTHENTICATED}" data-tab="edit">
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
                                        <td class="statistic">124</td>
                                        <td class="category">Organizer Since:</td>
                                        <td class="statistic">02/11/2017</td>
                                    </tr>
                                    <tr>
                                        <td class="category">Total Participants:</td>
                                        <td class="statistic">5201</td>
                                        <td class="category">Total Submissions:</td>
                                        <td class="statistic">73,240</td>
                                    </tr>
                                    <tr>
                                        <td class="category">Prize Money Awarded:</td>
                                        <td class="statistic">$65,500.00</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <h3>My Featured Competitions</h3>
                                <competition-tile each="{ sorted_competitions }" no-reorder
                                                  class="item"></competition-tile>
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
                                        <td class="statistic">1250</td>
                                        <td class="category">User Since:</td>
                                        <td class="statistic">09/12/2016</td>
                                    </tr>
                                    <tr>
                                        <td class="category">Top 10 Finishes:</td>
                                        <td class="statistic">1</td>
                                        <td class="category">Prize Money Won:</td>
                                        <td class="statistic">$2,500.00</td>
                                    </tr>
                                    <tr>
                                        <td class="category">Competitions Joined:</td>
                                        <td class="statistic">112</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="ui middle aligned unstackable no-margin compact divided link items content-desktop">
                                <h3>Latest Submissions</h3>
                                <competition-tile each="{ submissions }" class="item"></competition-tile>
                            </div>
                        </div>
                    </div>
                </div>
                <about-me></about-me>
                <div class="flex-content">
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
                                <td class="statistic">124</td>
                                <td class="category">Organizer Since:</td>
                                <td class="statistic">02/11/2017</td>
                            </tr>
                            <tr>
                                <td class="category">Total Participants:</td>
                                <td class="statistic">5201</td>
                                <td class="category">Total Submissions:</td>
                                <td class="statistic">73,240</td>
                            </tr>
                            <tr>
                                <td class="category">Prize Money Awarded:</td>
                                <td class="statistic">$65,500.00</td>
                            </tr>
                        </table>
                        <table class="stats-table">
                            <tr>
                                <td class="category">Submissions:</td>
                                <td class="statistic">1250</td>
                                <td class="category">User Since:</td>
                                <td class="statistic">09/12/2016</td>
                            </tr>
                            <tr>
                                <td class="category">Top 10 Finishes:</td>
                                <td class="statistic">1</td>
                                <td class="category">Prize Money Won:</td>
                                <td class="statistic">$2,500.00</td>
                            </tr>
                            <tr>
                                <td class="category">Competitions Joined:</td>
                                <td class="statistic">112</td>
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
                                <competition-tile each="{ sorted_competitions }" no-reorder
                                                  class="item"></competition-tile>
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
                                <competition-tile each="{ submissions }" class="item"></competition-tile>
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
            <div class="ui sixteen wide grid container">
                <div class="segment-container ui segment sixteen wide">
                    <div class="ui header">
                        My Submissions
                    </div>
                    <div class="container-content">
                        <div class="ui middle aligned unstackable compact divided link items content-desktop">
                            <competition-tile each="{ submissions }" class="item"></competition-tile>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!------------ EDIT TAB ----------->
        <div class="ui datasets tab" data-tab="datasets">
            <div class="ui sixteen wide grid container">
                <div class="segment-container datasets-segment ui segment sixteen wide">
                    <div class="ui header">
                        My Datasets
                    </div>
                    <div class="container-content">
                        <table class="ui celled table">
                            <thead>
                            <tr>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Uploaded</th>
                                <th>Public</th>
                                <th class="center aligned column">Delete</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td data-label="Name">file1.zip</td>
                                <td data-label="Type">Competition Bundle</td>
                                <td data-label="Uploaded">03/20/15</td>
                                <td data-label="Public">True</td>
                                <td data-label="Delete" class="center aligned column">
                                    <div class="ui red button">Delete</div>
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Name">file2.zip</td>
                                <td data-label="Type">Input Data</td>
                                <td data-label="Uploaded">11/20/2018</td>
                                <td data-label="Public">False</td>
                                <td data-label="Delete" class="center aligned column">
                                    <div class="ui red button">Delete</div>
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Name">file3.zip</td>
                                <td data-label="Type">Ingestion Program</td>
                                <td data-label="Uploaded">05/10/16</td>
                                <td data-label="Public">True</td>
                                <td data-label="Delete" class="center aligned column">
                                    <div class="ui red button">Delete</div>
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Name">file3.zip</td>
                                <td data-label="Type">Ingestion Program</td>
                                <td data-label="Uploaded">05/10/16</td>
                                <td data-label="Public">True</td>
                                <td data-label="Delete" class="center aligned column">
                                    <div class="ui red button">Delete</div>
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Name">file3.zip</td>
                                <td data-label="Type">Ingestion Program</td>
                                <td data-label="Uploaded">05/10/16</td>
                                <td data-label="Public">True</td>
                                <td data-label="Delete" class="center aligned column">
                                    <div class="ui red button">Delete</div>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
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
                            <div class="field" if="{!user.github_info}">
                                <label>Connect with github</label>
                                <a class="ui large blue button" href="/social/login/github">Login</a>
                            </div>
                            <div class="field" if="{!!user.github_info}">
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
                            <label class="email-pref">Subcribe to Email List to receive notifications</label>
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

        self.user = {
            github_info: '',
        }

        self.on('mount', function () {
            particlesJS.load('particles-js', "/static/particles/particles-profile.json", function () {
                console.log('callback - particles.js config loaded');
            })

            $('.secondary.pointing.menu .item').tab();
            $('.ui.checkbox').checkbox();
        })

        self.competitions = [
            {
                logo: 'http://placeimg.com/203/203/any',
                _obj_type: 'competition',
                title: 'Placeholder Competition',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '19',
                prize: '2400',
            },
            {
                logo: 'http://placeimg.com/204/204/any',
                _obj_type: 'competition',
                title: 'Placeholder Competition',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '1900',
                prize: '2400',
            },
            {
                logo: 'http://placeimg.com/205/205/any',
                _obj_type: 'competition',
                title: 'Placeholder Competition',
                description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit...",
                url: 'https://google.com/',
                start: '2018-01-29',
                end: '2021-06-29',
                participant_count: '190',
                prize: '2400',
            }
        ]

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
            }
        ]


        self.sorted_competitions = self.competitions.slice(0);
        self.sorted_competitions.sort(function (a, b) {
            return b.participant_count - a.participant_count;
        });


    </script>

    <style>
        .details {
            margin: 0 -1em
        }

        .competitions.tab .primary-container, .edit.tab .primary-container, about-me, events-container, organization-container {
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
        .edit.tab .container-content,
        .social-buttons {
            margin: 10px
        }

        #profile-menu {
            margin: 0
        }

        .competition-segment > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #f2faff;
            padding: 10px;
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
            padding: 30px;
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

        .competitions.tab .segment-container > .header, .datasets.tab .segment-container > .header, .edit.tab .segment-container > .header {
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

        .competitions.tab .list-tile, .edit.tab .list-tile {
            font-size: .75em
        }

        .competitions.tab .list-tile a, .edit.tab .list-tile a {
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

        .datasets .table {
            width: 100%
        }

        .datasets-segment {
            margin-top: 3em !important;
            width: 100%;
            padding: 0 !important
        }

        .datasets-segment .container-content {
            padding: 1em
        }

    </style>
</profile-page>

<about-me id="about-me">
    <div class="bio-segment primary-segment ui segment sixteen wide">
        <div class="ui header">
            About Me
            <div class="right floated ui button edit-button" onclick="{editing}" if="{!edit && USER_AUTHENTICATED}">
                Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{saving}" if="{!!edit && USER_AUTHENTICATED}">
                Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_edit}"
                 if="{!!edit && USER_AUTHENTICATED}">Cancel
            </div>
        </div>
        <div class="list-tile">
            <div class="biography">
                <div id="bio">{user.bio}</div>
                <div id="editor-container">
                    <textarea id="editor"></textarea>
                </div>
            </div>
        </div>
    </div>

    <script>
        var self = this

        self.user = {
            bio: "<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. A<strong>ccusantium adipisci aliquid assumenda beata</strong>e blanditiis consequuntur ducimus eum id, inventore laborum nemo nihil nisi provident qui quia rerum soluta tempore temporibus!</p>",
            bio_markdown: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. A**ccusantium adipisci aliquid assumenda beata**e blanditiis consequuntur ducimus eum id, inventore laborum nemo nihil nisi provident qui quia rerum soluta tempore temporibus!",
            github_info: '',
        }

        self.on('mount', function () {
            self.easymde = new EasyMDE({
                element: document.getElementById("editor"),
                renderingConfig: {
                    markedOptions: {
                        sanitize: true,
                    }
                }
            });

            $('#editor-container').hide()

            document.getElementById('bio').innerHTML = self.user.bio
        })

        self.editing = function () {
            $('#bio', self.root)
            self.edit = true
            self.easymde.value(self.user.bio_markdown);
            $('#editor-container').attr('style', 'display: block !important')
            self.easymde.codemirror.refresh();
        }

        self.saving = function () {
            self.edit = false
            self.user.bio_markdown = self.easymde.value()
            self.user.bio = marked(self.easymde.value())
            $('#editor-container').attr('style', 'display: none !important')
            document.getElementById('bio').innerHTML = self.user.bio
        }

        self.cancel_edit = function () {
            self.edit = false
            $('#editor-container').attr('style', 'display: none !important')
        }

        marked.setOptions({
            sanitize: true,
        })

    </script>

    <style>
        #editor-container {
            height: auto;
        }

        .primary-segment > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px;
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
            <div class="right floated ui button edit-button" onclick="{edit_education}"
                 if="{!edit_edu && USER_AUTHENTICATED}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_education}"
                 if="{!edit_edu && USER_AUTHENTICATED}">Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_education}"
                 if="{!!edit_edu && USER_AUTHENTICATED}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_education}"
                 if="{!!edit_edu && USER_AUTHENTICATED}">
                Cancel
            </div>
        </div>
        <div class="container-content">
            <education-tile></education-tile>
            <education-tile></education-tile>
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
        }

        .segment-container > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px;
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
    <div class="name">Placeholder University</div>
    <div class="degree">Bachelor's Degree, Test Science</div>
    <div class="attended">2007-2011</div>
    <div class="awards">Graduated Cum Laude with degrees in Testing Things and Science. Made
        Dean's List for 2 consecutive years.
    </div>
    <div class="ui divider"></div>
</education-tile>

<datasets-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Datasets
            <div class="right floated ui button edit-button" onclick="{edit_dataset}"
                 if="{!edit_dataset && USER_AUTHENTICATED}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_dataset}"
                 if="{!edit_dataset && USER_AUTHENTICATED}">Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_dataset}"
                 if="{!!edit_dataset && USER_AUTHENTICATED}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_dataset}"
                 if="{!!edit_dataset && USER_AUTHENTICATED}">Cancel
            </div>
        </div>
        <div class="container-content">
            <table class="ui striped table">
                <thead>
                <tr>
                    <th>Dataset</th>
                    <th>Date Uploaded</th>
                    <th>Downloads</th>
                    <th>File Size</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td><a href="#"><i class="download icon"></i>Cars</a></td>
                    <td>February 11, 2019</td>
                    <td>18</td>
                    <td>159mb</td>
                </tr>
                <tr>
                    <td><a href="#"><i class="download icon"></i>Numbers</a></td>
                    <td>June 18, 2018</td>
                    <td>104</td>
                    <td>1.34gb</td>
                </tr>
                <tr>
                    <td><a href="#"><i class="download icon"></i>Animals</a></td>
                    <td>January 11, 2018</td>
                    <td>2011</td>
                    <td>416mb</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
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
            padding: 10px;
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

<organization-container class="primary-container">
    <div class="segment-container ui segment sixteen wide">
        <div class="ui header">
            My Organizations
            <div class="right floated ui button edit-button" onclick="{edit_organization}"
                 if="{!edit_organization && USER_AUTHENTICATED}">
                Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_organization}"
                 if="{!edit_organization && USER_AUTHENTICATED}">
                Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_organization}"
                 if="{!!edit_organization && USER_AUTHENTICATED}">
                Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_organization}"
                 if="{!!edit_organization && USER_AUTHENTICATED}">
                Cancel
            </div>
        </div>
        <div class="container-content">
            <organization-tile></organization-tile>
            <organization-tile></organization-tile>
        </div>
    </div>

    <script>
    </script>

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
            padding: 10px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px #dcdcdc
        }

        .container-content {
            margin: 20px
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
            <div class="right floated ui button edit-button" onclick="{edit_events}"
                 if="{!edit_events && USER_AUTHENTICATED}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_events}"
                 if="{!edit_events && USER_AUTHENTICATED}">Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_events}"
                 if="{!!edit_events && USER_AUTHENTICATED}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_events}"
                 if="{!!edit_events && USER_AUTHENTICATED}">Cancel
            </div>
        </div>
        <div class="container-content">
            <events-tile></events-tile>
            <events-tile></events-tile>
        </div>
    </div>

    <script>
    </script>

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
            padding: 10px;
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

    <script>
    </script>

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