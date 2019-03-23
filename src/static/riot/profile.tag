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
                        <div class="occupation">Programmer at MadeUp Company</div>
                        A brief description of the user goes here
                    </div>
                    <!-- <div class="ui large button msg-btn">Message Me</div>
                    <span class="ui icon large button follow-btn"><i class="user icon"></i>Follow</span> -->
                </div>
                <recent-container></recent-container>
            </div>
            <div id="profile-menu" class="ui secondary pointing menu">
                <a class="active item" data-tab="home">
                    Home
                </a>
                <a class="item" data-tab="edit">
                    Add/Edit
                </a>
            </div>
        </div>


        <!------------ HOME TAB ----------->
        <div class="ui active home tab" data-tab="home">
            <div class="ui sixteen wide grid container">
                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Competitions</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Competition ended 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Competition ended 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Competition ended 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Competition ended 03/01/2018</div>
                            </div>
                        </div>
                        <div class="scores">
                            <div class="medals">
                                <div class="medal medal-one"></div>
                                <div class="medal medal-two"></div>
                                <div class="medal medal-three"></div>
                            </div>
                            <div class="medal-amounts">
                                <div class="medal-amount">12</div>
                                <div class="medal-amount">18</div>
                                <div class="medal-amount">43</div>
                            </div>
                            <table class="stats">
                                <tr>
                                    <td class="category">Competitions:</td>
                                    <td class="statistic">124</td>
                                </tr>
                                <tr>
                                    <td class="category">Percentile:</td>
                                    <td class="statistic">89.25</td>
                                </tr>
                                <tr>
                                    <td class="category">Total Score:</td>
                                    <td class="statistic">12,389.25</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="competition-segment ui segment eight wide">
                    <div class="ui header">Submissions</div>
                    <div class="ui content flex-content">
                        <div class="list-comps">
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Submitted 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Submitted 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Submitted 03/01/2018</div>
                            </div>
                            <div class="list-tile">
                                <a href="#">Competition about competition b...</a>
                                <div class="date-complete">Submitted 03/01/2018</div>
                            </div>
                        </div>
                        <div class="scores">
                            <div class="medals">
                                <div class="medal medal-one"></div>
                                <div class="medal medal-two"></div>
                                <div class="medal medal-three"></div>
                            </div>
                            <div class="medal-amounts">
                                <div class="medal-amount">12</div>
                                <div class="medal-amount">18</div>
                                <div class="medal-amount">43</div>
                            </div>
                            <table class="stats">
                                <tr>
                                    <td class="category">Submissions:</td>
                                    <td class="statistic">124</td>
                                </tr>
                                <tr>
                                    <td class="category">Percentile:</td>
                                    <td class="statistic">89.25</td>
                                </tr>
                                <tr>
                                    <td class="category">Total Score:</td>
                                    <td class="statistic">12,389.25</td>
                                </tr>
                            </table>
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

        <!------------ EDIT TAB ----------->
        <div class="ui edit tab" data-tab="edit">
            <div class="ui equal width grid container">
                <div class="ui form">
                    <div class="profile-row">
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

    </script>

    <style>
        .home {
            margin: 0 -1em;
        }

        about-me {
            width: 100%;
        }

        education-container {
            width: 40% !important;
        }

        datasets-container {
            width: 57.5%;
        }

        organization-container {
            width: 100%;
        }

        events-container {
            width: 100%;
        }

        recent-container {
            margin: 1em 1em 1em auto;
            text-align: right;
            float: right;
        }

        .home > .container {
            margin-top: 1em;
        }

        #editor-container {
            height: auto;
        }

        .stats .category {
            font-weight: 600;
            font-size: 1.15em;
            color: #202d53;
            text-align: right;
        }

        .stats .statistic {
            width: 100%;
            font-size: .85em;
            color: #A0A0A0;
            text-align: right;
        }

        .home > .container > .ui.segment {
            width: 47.5%;
            margin: 1em;
            padding: 0;
        }

        .occupation {
            font-weight: 600;
        }

        .social-buttons {
            margin: 10px;
        }

        #profile-menu {
            margin: 0;
        }

        .competition-segment > .header {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            background-color: #F2FAFF;
            padding: 10px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            border-bottom: solid 1px gainsboro;
        }

        .competition-segment {
            margin: 15px 0;
        }

        .bio-segment {
            width: 100% !important;
        }

        .biography {
            padding: 30px;
            color: #A0A0A0;
        }

        .flex-content {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            flex-wrap: wrap;
            margin: 1em 0;
        }

        .list-tile > a {
            font-size: 15px;
            font-weight: 600;
        }

        .list-comps {
            border-right: 1px solid gainsboro;
            width: 60%;
        }

        .list-comps, .scores {
            padding: 20px;
        }

        .medals, .medal-amounts {
            display: flex;
            flex-direction: row;
        }

        .medal {
            height: 30px;
            width: 30px;
            margin: 3px 14px;
        }

        .medal-one {
            background-image: url('/static/img/gold_medal.svg');
        }

        .medal-two {
            background-image: url('/static/img/silver_medal.svg')
        }

        .medal-three {
            background-image: url('/static/img/bronze_medal.svg')
        }

        .medal-amount {
            text-align: center;
            margin: 14px;
            width: 30px;
        }

        .date-complete {
            color: #A0A0A0;
            font-size: 0.8em;
        }

        .education-container {
            width: 33% !important;
        }

        .datasets-container {
            width: 60% !important;
        }
    </style>
</profile-page>

<about-me id="about-me">
    <div class="bio-segment primary-segment ui segment sixteen wide">
        <div class="ui header">
            About Me
            <div class="right floated ui button edit-button" onclick="{editing}" if="{!edit}">Edit</div>
            <div class="right floated ui button edit-button" onclick="{saving}" if="{!!edit}">Save</div>
            <div class="right floated ui button edit-button" onclick="{cancel_edit}" if="{!!edit}">Cancel</div>
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
            self.simplemde = new SimpleMDE({
                element: document.getElementById("editor")
            });

            $('#editor-container').hide()

            document.getElementById('bio').innerHTML = self.user.bio
        })

        self.editing = function () {
            $('#bio', self.root)
            self.edit = true
            self.simplemde.value(self.user.bio_markdown);
            $('#editor-container').attr('style', 'display: block !important')
            self.simplemde.codemirror.refresh();
        }

        self.saving = function () {
            self.edit = false
            self.user.bio_markdown = self.simplemde.value()
            self.user.bio = marked(self.simplemde.value())
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
            <div class="right floated ui button edit-button" onclick="{edit_education}" if="{!edit_education}">Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_education}" if="{!edit_education}">Add</div>
            <div class="right floated ui button edit-button" onclick="{save_education}" if="{!!edit_education}">Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_education}" if="{!!edit_education}">
                Cancel
            </div>
        </div>
        <div class="container-content">
            <education-tile></education-tile>
            <education-tile></education-tile>
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
            <div class="right floated ui button edit-button" onclick="{edit_dataset}" if="{!edit_dataset}">Edit</div>
            <div class="right floated ui button edit-button" onclick="{add_dataset}" if="{!edit_dataset}">Add</div>
            <div class="right floated ui button edit-button" onclick="{save_dataset}" if="{!!edit_dataset}">Save</div>
            <div class="right floated ui button edit-button" onclick="{cancel_dataset}" if="{!!edit_dataset}">Cancel
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
            <div class="right floated ui button edit-button" onclick="{edit_organization}" if="{!edit_organization}">
                Edit
            </div>
            <div class="right floated ui button edit-button" onclick="{add_organization}" if="{!edit_organization}">
                Add
            </div>
            <div class="right floated ui button edit-button" onclick="{save_organization}" if="{!!edit_organization}">
                Save
            </div>
            <div class="right floated ui button edit-button" onclick="{cancel_organization}" if="{!!edit_organization}">
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
            <div class="right floated ui button edit-button" onclick="{edit_events}" if="{!edit_events}">Edit</div>
            <div class="right floated ui button edit-button" onclick="{add_events}" if="{!edit_events}">Add</div>
            <div class="right floated ui button edit-button" onclick="{save_events}" if="{!!edit_events}">Save</div>
            <div class="right floated ui button edit-button" onclick="{cancel_events}" if="{!!edit_events}">Cancel</div>
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