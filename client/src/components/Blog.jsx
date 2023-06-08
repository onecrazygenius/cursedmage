import React from 'react';
import { useState } from 'react'

import Popup from './Popup'

const Blog = ({props}) => {

    const [openPopup, setOpenPopup] = useState(false);

    const { title, content, image } = props;
    const preview = content.substring(0, 100) + "...";

    const imageURL = "/images/" + image;

    const toggle = () => {
        setOpenPopup(!openPopup);
    }

    return ( 
    <div class="blog">
        <a onClick={toggle}>
            <img src={imageURL} alt="blog" />
        </a>
        <div class="bio">
            <h2>{title}</h2>
            <a onClick={toggle} class="button">Read</a>
            <p>{preview}</p>
        </div>

        {openPopup && <Popup props={props} setOpenPopup={setOpenPopup} />}
    </div> 
    );
}
 
export default Blog;