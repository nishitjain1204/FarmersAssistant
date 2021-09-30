import React, { Fragment } from "react";
import Header from "../layout/Header";
import axios from "axios";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Grid from "@material-ui/core/Grid";
import { spacing } from "@material-ui/system";
const News = ({ news }) => {
  var news = Object.values(news);
  return (
    <div>
      <Grid container justify="center" spacing={4}>
        {news.map((item) => (
          <>
            <Grid key={item.id} item xs={12} sm={6} md={4} lg={3}>
              <Card sx={{ maxWidth: 345 }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={item.image}
                  alt="green iguana"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    News
                  </Typography>
                  <Typography noWrap variant="body2" color="text.secondary">
                    {item.summary}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button mt={7} size="small">
                    Share{" "}
                  </Button>
                  <Button href={item.link} variant="contained" size="small">
                    Learn More
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </>
        ))}
      </Grid>
    </div>
  );
};
export default News;
