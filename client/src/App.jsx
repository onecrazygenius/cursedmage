import { useState } from 'react'
import Blog from './components/Blog'
import Member from './components/Member'
import Leaderboard from './components/Leaderboard'

function App() {

    const [blogs, setBlogs] = useState([
        {
            title: "MVP Day! 26/08",
            content: "It is the 1.0.0a release of the game! We have completed an intensive round of testing and the introduction of \
            many new features since the last live demo of our game, like animations, bosses and a vast dungeon to explore. We bring to \
            you the most fun, action packed release yet! Are you Excited? Because we are, checkout the game via the download button above!",
            image: "welcome.png"
        },
        {
            title: "Overhaul! 26/07",
            content: "Get ready to experience Cursed Mage like never before! Our latest update brings an exciting twist to your gameplay, \
            introducing a complete overhaul of the map system. Say farewell to the old static grids and step into the realm of dynamically \
            generated dungeon maps. Brace yourself for a fresh challenge with every ascent as no two dungeons are alike. Your path will be \
            concealed, testing your skills and intuition to the fullest. Adapt, strategize, and collect the most powerful artefacts by slaying \
            bosses, unleashing their full power.",
            image: "welcome.png"
        },
        {
            title: "Big changes! 29/06",
            content: "Welcome to the new and improved cursed mage! We have added a leaderboard system where you and all \
            of your friends can compete to get the top score! When you go through the dungeons, defeat the mighty enemies \
            and come out victorious your score will go up each battle you win, don't think it will be a walk in the park though \
            the enemies will get stronger and them cursed cards will fill up your inventory so be careful not to fall into the \
            depths of the dungeon!",
            image: "welcome.png"
        },
        {
            title: "New Magic! 02/06",
            content: "Introducing the Cursed Mage's revolutionary deck building feature! \
            In this immersive game, each character possesses a distinctive deck, creating endless strategic possibilities. But that's not all - we've recently added an exciting twist. \
            Now, players can handpick a card of their choice upon vanquishing an adversary, enhancing their arsenal and empowering their gameplay. With this new addition, the Cursed Mage offers an unparalleled level of customization and rewards skillful combat. \
            Embrace the challenge, assemble your perfect deck, and become the ultimate mage in this enchanting world of magic and adventure. \
            In our quest to deliver an immersive world the biggest challenge was creating backgrounds that portrays the theme, we agreed that our background should be based off of something dark or cold as that allows us to give the correct theme before we started. \
            In doing this we could add detail and make the backgrounds much more interesting and immersive without having to fixate on dark and cold themes. \
            This will create an overall improvement in your experience as there will be a lot more variety in the surroundings of the character. ",
            image: "magic.png"
        },
        {
            title: "Switch Up! 28/04",
            content: "We have made an amazing switch from Unity to Python for our game development. \
            We encountered a range of blockers when developing our game with Unity such as lack of motivation which resulted in a lack of contributions towards the game development. \
            The Strategic Switch motivated all our developers to contribute towards the game and we found that they were happier with a coding language and game development method that they were familiar with. \
            Progress is now astonishingly quick and we look forward to showing off our results in the upcoming MVP day. \
            In our creation of Cursed Mage we started out with a cartoonish art style but quickly realized it would not match with the game we wanted to make and was unrealistic for us to turn over large amounts or quality art. \
            Because of this we decided to transition to a pixel art style which gave us the opportunity to create a lot of quality artwork that fits the game perfectly \
            We view this change as a part of the games journey and believe it will improve you experience dramatically while playing the game. \
            Look out for the MVP alpha release on the 9th of June!",
            image: "python.png"
        },
        {
            title: "Welcome! 18/02",
            content: "We began our journey in December 2022, and we are now in the process of building our game. \
                        We have a lot of work to do, but we are confident that we will be able to deliver a game \
                        that will be fun and enjoyable for all players. Since our inception we have put together a \
                        hack of the game to start bringing together something that fits the scope of this game - and can help \
                        us start to make something we know you will love. We are going to continue to work on the game in the background but have done alot of the \
                        heavy lifting in planning and designing something we know you will love. \
                        We hope to catch you all in our alpha release soon!",
            image: "welcome.png"
        }
    ])

    const [members, setMembers] = useState([
        {
            name: "Charlie",
            bio: "Lead Developer",
            image: "charlie.png"
        },
        {
            name: "James",
            bio: "Project Manager",
            image: "james.png"
        },
        {
            name: "Duvina",
            bio: "Artist & Web Design",
            image: "duvina.png"
        },
        {
            name: "Morgan",
            bio: "Artist",
            image: "morgan.png"
        },
        {
            name: "Massimo",
            bio: "Developer",
            image: "massimo.png"
        },
        {
            name: "Dev",
            bio: "Developer",
            image: "dev.png"
        },
        {
            name: "Flavia",
            bio: "Developer",
            image: "flavia.png"
        }
    ])

    return (
    <div className="container">
        <div className="parallax-wrapper">
            <div className="logo">
                <img src="images/cursedmage.svg" />
                <a className="button" href="/dist/CursedMage.exe" target="_blank" download>Play Now!</a>
            </div>
            <div className="parallax" id="level0"></div>
            <div className="parallax" id="level1"></div>
            <div className="parallax" id="level2"></div>
            <div className="parallax" id="level3"></div>
        </div>
        <div className="content">
            <h2>
                Cursed Mage is a dungeon full of magic, demons and roguelike action.<br /><br />
                Your character has been kidnapped and lost their power! The world is falling apart and people are DYING! Someone needs to be a hero! But who?
            </h2>
            <hr />
            <Leaderboard />
            <hr />
            <h2 className="title">
                Blogs
            </h2>
            <div className="blogs">
                {blogs.map((blog, index) => (
                    <Blog key={index} props={blog} />
                ))}
            </div>
            <hr />
            <h2 className="title">
                About
            </h2>
            <div className="blogs">
                {members.map((member, index) => (
                    <Member key={index} props={member} />
                ))}
            </div>
        </div>
        <small class="footer">(c) Cursed Mage</small>
    </div>
  )
}

export default App;
