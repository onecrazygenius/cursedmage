import React from 'react';

const Popup = ({props, setOpenPopup}) => {

    const { title, content, image } = props;

    const imageURL = "/images/" + image;

    const closePopup = () => {
        setOpenPopup(false);
    }

    return ( 
        <div className="popup">
            <div className="popup-content">
                <img src={imageURL} alt="blog" />
                <h2>{title}</h2>
                <p>{content}</p>
                <a onClick={closePopup} className="close">&times;</a>
            </div>
        </div>
    );
}
 
export default Popup;