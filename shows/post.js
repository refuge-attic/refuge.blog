function(doc, req) {
    var Mustache = require("lib/mustache");
    var Markdown = require("lib/markdown");
    
    var ddoc = this;
    var templates = ddoc.templates;
    
    provides("html", function() {
        var row;
        var full_posts = [];
        var post_links = [];
        //while(row = getRow()) {
        //    var doc = row.value;
            
            var post_link = {
                "title": doc.title,
                "date": doc.created_at
            }
            post_links.push(post_link);
            
            var post = doc;
            post.body = Markdown.encode(post.body);
            full_posts.push({"full": Mustache.to_html(templates.post, post)});
        //}
        
        return Mustache.to_html(templates.posts, {
            "full_posts": full_posts,
            "post_links": post_links
        });
    });
}