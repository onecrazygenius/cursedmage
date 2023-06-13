import React from 'react';

const Member = ({props}) => {


    const { name, bio, image } = props;

    const imageURL = `images/${image}`;

    return ( 
    <div class="blog member">
        <a className="image_wrap">
            <img src={imageURL} />
        </a>
        <div class="bio">
            <h2>{name}</h2>
            <a class="button">{bio}</a>
        </div>
    </div> 
    );
}
 
export default Member;