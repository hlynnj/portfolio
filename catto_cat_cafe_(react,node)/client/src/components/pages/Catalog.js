import React, { useState, useEffect } from "react";
import CatProfile from "../modules/CatProfile.js";
import CatalogCard from "../modules/CatalogCard.js";
import BackButton from "../modules/BackButton.js";
import { get } from "../../utilities";
import "./Catalog.css";
const Catalog = (props) => {
  useEffect(() => {
    get("/api/resetcatalog");
  });

  const [activeProfile, setActiveProfile] = useState({
    name: "Arthur",
    img: "https://i.ibb.co/GphN5Ck/arthur-full.png",
    description_type: "Black and white",
    description_likes: "Sitting on books",
    description_dislikes: "Doctor's visits",
    description_personality:
      "Runs fast and has a strong kick. Arthur is an extremely intelligent cat, but you almost wouldn’t be able to tell for all the danger he seems to run headfirst into except for the fact that there’s no way a normal cat would get himself into such situations in the first place. Dashing away from not one, but five dogs at the same time, balancing precariously on the windowsills of restricted properties, trying to lick suspicious-looking powders… the list goes on. But hey, sometimes he also finds and brings back your lost items when you need them most, so he’s not so bad to have around.",
  });

  const loadCatProfile = (catname) => {
    get("/api/catprofile", { cat_name: catname }).then((catinfo) => {
      setActiveProfile({
        name: catinfo[0].name,
        img: catinfo[0].full,
        description_type: catinfo[0].description_type,
        description_likes: catinfo[0].description_likes,
        description_dislikes: catinfo[0].description_dislikes,
        description_personality: catinfo[0].description_personality,
      });
    });
  };

  return (
    <div className="full_screen">
      <div className="catalog-header">
        <div className="catalog-backbutton">
          <BackButton link="/home" text="<Back" />{" "}
        </div>
        <div className="catalog-header-name header-name-withback"> Catalog</div>
      </div>
      <div className="catalog_container">
        <div className="row u-flex">
          <div className="catalog-nav-column catalog-column">
            {
              // all these are place holders.
              // TODO: once we get to getting all cat data
              // we can do the thing where it's like
              // for each cata we obtain from the DB
              // we add a CatalogCard element into an array
              // and we render the array
            }
            <div className="catalog-cards-list-container u-flex u-flexColumn">
              <CatalogCard
                img="https://i.ibb.co/znTpDNb/arthur-head.png"
                name="Arthur"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/x13gvbc/box-head.png"
                name="Box"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/TKrTTgz/brioche-head.png"
                name="Brioche"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/wpvjGmf/cardigan-head.png"
                name="Cardigan"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/Q6Nr45z/clover-head.png"
                name="Clover"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/Vxjsd9b/dana-head.png"
                name="Dana"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/Gk5TJNw/finnegan-head.png"
                name="Finnegan"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/RD18rZR/lily-head.png"
                name="Lily"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/mDJ6LvQ/margaret-head.png"
                name="Margaret"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/kyDbMZb/pearl-head.png"
                name="Pearl"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/8M93yFf/pompom-head.png"
                name="PomPom"
                loadCatProfile={loadCatProfile}
              />
              <CatalogCard
                img="https://i.ibb.co/cJvpH5k/ritz-head.png"
                name="Ritz"
                loadCatProfile={loadCatProfile}
              />
            </div>
          </div>
          <div className="catalog-static-column catalog-column">
            <div className="catalog-profile-container">
              <CatProfile
                img={activeProfile.img}
                name={activeProfile.name}
                description_type={activeProfile.description_type}
                description_likes={activeProfile.description_likes}
                description_dislikes={activeProfile.description_dislikes}
                description_personality={activeProfile.description_personality}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Catalog;
