import { useState } from 'react'
import Blog from './components/Blog'

function App() {

    const [blogs, setBlogs] = useState([
        {
            title: "Blog 1",
            content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl vitae aliquam ultricies, nunc nisl ultricies nunc, vit",
            image: "blog1.jpg"
        },
        {
            title: "Blog 2",
            content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl vitae aliquam ultricies, nunc nisl ultricies nunc, vit",
            image: "blog2.jpg"
        },
        {
            title: "Blog 3",
            content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl vitae aliquam ultricies, nunc nisl ultricies nunc, vit",
            image: "blog3.jpg"
        }
    ])
    return (
    <div className="container">
        <div className="parallax-wrapper">
            <div className="logo">
                <img src="images/cursedmage.svg" />
                <a className="button" href="/dist/CursedMage.exe" target="_blank" download>Play the Demo Now</a>
            </div>
            <div className="parallax" id="level0"></div>
            <div className="parallax" id="level1"></div>
            <div className="parallax" id="level2"></div>
            <div className="parallax" id="level3"></div>
        </div>
        <div className="content">
            <h2>
                Cursed Mage is a dungeon full of magic, demons and roguelike action.<br /><br />
                Your blog has been kidnapped and lost their power! The world is falling apart and people are DYING! Someone needs to be a hero! But who?
            </h2>
            <hr></hr>
            <h2 className="title">
                Blogs
            </h2>
            <div class="blogs">
                {blogs.map((blog, index) => (
                    <Blog key={index} props={blog} />
                ))}
            </div>
            <hr />
            <h2 className="title">
                About
            </h2>
        </div>
        <small class="footer">(c) Cursed Mage</small>
    </div>
  )
}

export default App;
