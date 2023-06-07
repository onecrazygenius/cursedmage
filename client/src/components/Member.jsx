import React from 'react';

const Member = ({props}) => {


    const { name, bio, image } = props;

    return ( 
    <div class="blog member">
        <a className="image_wrap">
            <img src="images/{image}" />
            <p>{bio}</p>
        </a>
        <div class="bio">
            <h2>{name}</h2>
        </div>
    </div> 
    );
}
 
export default Member;