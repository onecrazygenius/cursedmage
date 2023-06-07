import React from 'react';

const Popup = ({props, setOpenPopup}) => {

    const { title, content, image } = props;

    const closePopup = () => {
        setOpenPopup(false);
    }

    return ( 
        <div className="popup">
            <div className="popup-content">
                <img src="images/{image}"/>
                <h2>{title}</h2>
                <p>{content}</p>
                <a onClick={closePopup} className="close">&times;</a>
            </div>
        </div>
    );
}
 
export default Popup;