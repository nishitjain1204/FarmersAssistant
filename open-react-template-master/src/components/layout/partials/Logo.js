import React from "react";
import classNames from "classnames";
import { Link } from "react-router-dom";
import Image from "../../elements/Image";

const Logo = ({ className, ...props }) => {
  const classes = classNames("brand", className);

  return (
    <div {...props} className={classes}>
      <h1 className="m-0">
        <Link to="/">
          <Image
            src={require("./../../../assets/images/mainLogo.png")}
            alt="Open"
            width={82}
            height={82}
            // style={
            //   bord
            // }
          />
        </Link>
      </h1>
    </div>
  );
};

export default Logo;
