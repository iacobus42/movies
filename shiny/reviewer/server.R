shinyServer(function(input, output) {
    library(ggplot2)
    library(scales)
    library(DBI)
    library(RMySQL)   
    m <- dbDriver("MySQL");
    con2 <- dbConnect(m, user='simmerin', 
                      password='simmerin',
                      host='localhost',
                      dbname='movies')
    output$comp_plot <- renderPlot({
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        reviews <- dbGetQuery(con2, "select rtid, reviewer, fresh from reviews")
        timing <- dbGetQuery(con2, "select id, month, year from mojo")
        link <- dbGetQuery(con2, "select id, rtid from rtid")
        reviews <- reviews[reviews$reviewer == input$critic, ]
        scores <- scores[scores$rtid %in% reviews$rtid, ]
        genres <- genres[genres$rtid %in% reviews$rtid, ]
        link <- link[link$rtid %in% reviews$rtid, ]
        timing <- timing[timing$id %in% link$id, ]
        
        outletData <- merge(reviews, scores, by = "rtid")
        outletData <- merge(outletData, link, by = "rtid")
        outletData <- merge(outletData, timing, by = "id")
        genreData <- merge(reviews, genres, by = "rtid")
        
        outletData$date <- as.Date(paste(outletData$year, outletData$month, 
                                         "1", sep = "-"))
        
        mByG <- aggregate(genreData$fresh, list(genreData$genre), mean)
        cByG <- aggregate(rep(1, length(genreData$genre)), 
                          list(genreData$genre),
                          sum)
        
        mByM <- aggregate(outletData$fresh, list(outletData$date), mean)
        cByM <- aggregate(rep(1, length(outletData$date)), 
                          list(outletData$date), 
                          sum)
        oByM <- aggregate(outletData$criticScore,
                          list(outletData$date),
                          mean)
        names(mByM) <- c("date", "fresh")
        names(oByM) <- c("date", "otherScore")
        compare <- merge(mByM, oByM, by = "date")
        compPlot <- ggplot() + 
            geom_point(aes(y = fresh, x = criticScore), data = outletData) + 
            geom_smooth(aes(y = fresh, x = criticScore), data = outletData, 
                        method = "loess", alpha = 0) + 
            theme_bw() + 
            scale_x_continuous("Mean Critic Score") + 
            scale_y_continuous("Publication Score", limits = c(0, 1)) + 
            geom_abline(slope = 1/100, lty = 2)
        print(compPlot)
    })
    output$time_plot <- renderPlot({
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        reviews <- dbGetQuery(con2, "select rtid, reviewer, fresh from reviews")
        timing <- dbGetQuery(con2, "select id, month, year from mojo")
        link <- dbGetQuery(con2, "select id, rtid from rtid")
        reviews <- reviews[reviews$reviewer == input$critic, ]
        scores <- scores[scores$rtid %in% reviews$rtid, ]
        genres <- genres[genres$rtid %in% reviews$rtid, ]
        link <- link[link$rtid %in% reviews$rtid, ]
        timing <- timing[timing$id %in% link$id, ]
        
        outletData <- merge(reviews, scores, by = "rtid")
        outletData <- merge(outletData, link, by = "rtid")
        outletData <- merge(outletData, timing, by = "id")
        genreData <- merge(reviews, genres, by = "rtid")
        
        outletData$date <- as.Date(paste(outletData$year, outletData$month, 
                                         "1", sep = "-"))
        
        mByG <- aggregate(genreData$fresh, list(genreData$genre), mean)
        cByG <- aggregate(rep(1, length(genreData$genre)), 
                          list(genreData$genre),
                          sum)
        
        mByM <- aggregate(outletData$fresh, list(outletData$date), mean)
        cByM <- aggregate(rep(1, length(outletData$date)), 
                          list(outletData$date), 
                          sum)
        oByM <- aggregate(outletData$criticScore,
                          list(outletData$date),
                          mean)
        names(mByM) <- c("date", "fresh")
        names(oByM) <- c("date", "otherScore")
        compare <- merge(mByM, oByM, by = "date")
        timePlot <- ggplot() + 
            geom_line(aes(x = date, y = fresh), data = mByM, 
                      alpha = 0.5) + 
            geom_point(aes(x = date, y = fresh), size = cByM$x, 
                       data = mByM) + 
            geom_smooth(aes(x = date, y = fresh), data = mByM, 
                        method = "loess", alpha = 0, size = 2) + 
            theme_bw() + 
            scale_x_date("", breaks = "1 years", labels = date_format("%Y")) +
            scale_y_continuous("Monthly Mean Score")
        print(timePlot)
    })
    output$genre_plot <- renderPlot({
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        reviews <- dbGetQuery(con2, "select rtid, reviewer, fresh from reviews")
        timing <- dbGetQuery(con2, "select id, month, year from mojo")
        link <- dbGetQuery(con2, "select id, rtid from rtid")
        reviews <- reviews[reviews$reviewer == input$critic, ]
        scores <- scores[scores$rtid %in% reviews$rtid, ]
        genres <- genres[genres$rtid %in% reviews$rtid, ]
        link <- link[link$rtid %in% reviews$rtid, ]
        timing <- timing[timing$id %in% link$id, ]
        
        outletData <- merge(reviews, scores, by = "rtid")
        outletData <- merge(outletData, link, by = "rtid")
        outletData <- merge(outletData, timing, by = "id")
        genreData <- merge(reviews, genres, by = "rtid")
        
        outletData$date <- as.Date(paste(outletData$year, outletData$month, 
                                         "1", sep = "-"))
        
        mByG <- aggregate(genreData$fresh, list(genreData$genre), mean)
        cByG <- aggregate(rep(1, length(genreData$genre)), 
                          list(genreData$genre),
                          sum)
        
        mByM <- aggregate(outletData$fresh, list(outletData$date), mean)
        cByM <- aggregate(rep(1, length(outletData$date)), 
                          list(outletData$date), 
                          sum)
        oByM <- aggregate(outletData$criticScore,
                          list(outletData$date),
                          mean)
        names(mByM) <- c("date", "fresh")
        names(oByM) <- c("date", "otherScore")
        compare <- merge(mByM, oByM, by = "date")
        genrePlot <- ggplot() + 
            geom_point(aes(x = Group.1, y = x), data = mByG, size = log(cByG$x) / max(log(cByG$x)) * 5) + 
            theme_bw() + 
            scale_x_discrete(name = "") + 
            scale_y_continuous("Mean Score") + 
            theme(axis.text.x = element_text(angle = 90))
        print(genrePlot)        
    })
})