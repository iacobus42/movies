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
    output$genre_plot <- renderPlot({
        ids  <- dbGetQuery(con2, "select id, rtid from rtid")
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2)
        
        genres <- genres[genres$genre == input$genre, ]
        scores <- scores[scores$rtid %in% genre$rtid, ]
        data <- merge(ids, scores, by = "rtid")
        data <- merge(data, dates, by = "id")
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        mByM <- aggregate(data$criticScore, list(data$date), mean, na.rm = TRUE)
        cByM <- aggregate(rep(1, length(data$date)), list(data$date), sum)
        p <- ggplot() + 
            geom_point(aes(x = as.Date(date, "%Y-%m-%d"), y = criticScore), data = data, alpha = 0.1) + 
            geom_line(aes(x = as.Date(Group.1, "%Y-%m-%d"), y = x), 
                       data = mByM, size = 1) + 
            geom_smooth(aes(x = date, y = criticScore), data = data, method = "lm") + 
            theme_bw() +
            scale_x_date("", breaks = "1 years", labels = date_format("%Y")) + 
            scale_y_continuous("Critic Score")
            
        print(p)
    })
})