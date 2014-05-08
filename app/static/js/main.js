var Line = Backbone.Model.extend({
    defaults: {
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": 0,
        "hover": false
    }
});

var Lines = Backbone.Collection.extend({
    model: Line
});

var lines = new Lines();

$(function(){
    var img = $('#theimage');

    var canvas = document.getElementById("canvas"),
        ctx = canvas.getContext("2d"),
        drawCanvas = document.getElementById("drawCanvas"),
        drawCtx = drawCanvas.getContext("2d"),
        started = false,
        lastX = 0,
        lastY = 0,
        curX = 0,
        curY = 0,
        startX = 0,
        startY = 0,
        lineThickness = 1
        width = img.width(),
        height = img.height();

    canvas.width = drawCanvas.width = width;
    canvas.height = drawCanvas.height = height;

    drawCanvas.onmousedown = function(e){
        if(started){
            started = false;
            lastX = e.pageX - this.offsetLeft - 10;
            lastY = e.pageY - this.offsetTop - 10;
            
            clearCxt(drawCtx);
            lines.add(new Line({x1: startX, y1: startY, x2: lastX, y2:lastY}));
        } else {
            started = true;
            startX = e.pageX - this.offsetLeft - 10;
            startY = e.pageY - this.offsetTop - 10;

            drawCircle(drawCtx, startX, startY);
        }
    };

    lines.on('add', function(){
        drawAllLines(ctx, lines);
    });

    lines.on('change', function(){
        drawAllLines(ctx, lines);
    });

    lines.on('remove', function(){
        drawAllLines(ctx, lines);
    });

    var Edit = Backbone.View.extend({
        tagName: 'div',

        template: _.template($('#edit-template').html()),

        events: {
            "change input": "update",
            "click a.delete": "delete",
            "mouseover .view": "hovered",
            "mouseleave .view": "unhovered"
        },

        initialize: function(){
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },

        update: function(e){
            newX1 = this.$('input.x1').val();
            newY1 = this.$('input.y1').val();
            newX2 = this.$('input.x2').val();
            newY2 = this.$('input.y2').val();
            this.model.set({'x1': newX1, 'y1': newY1, 'x2': newX2, 'y2': newY2});
        },

        delete: function(){
            this.model.destroy();
            return false;
        },

        hovered: function(){
            this.model.set({'hover': true})
        },

        unhovered: function(){
            this.model.set({'hover': false})
        }
    });

    var Edits = Backbone.View.extend({
        el: $('#edits'),

        events: {
            "click #save": "persist"
        },

        initialize: function(){
            this.$('#width').html(width);
            this.$('#height').html(height);
            this.listenTo(lines, 'add', this.addOne);
            this.retrieve();

        },

        addOne: function(line){
            var edit = new Edit({model: line});
            this.$el.append(edit.render().el);
        },

        persist: function(){
            lines_json = lines.toJSON();
            to_send = JSON.stringify(lines_json)
            $.ajax({
                url: '/s/' + subd + '/' + img_name,
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: to_send,
            })
            .done(function(){
                $('#save').css('background-color', '#FFDC00')
            })
            .fail(function(e){
                alert('error in persist');
                console.log(e);
            });
            return false;
        },

        retrieve: function(){
            $.ajax({
                url: '/g/' + subd + '/' + img_name,
                type: 'GET',
                dataType: 'json',
            })
            .done(function(e) {
                if (e.has) {
                    lines_parsed = lines.parse(e.lines);
                    for (var i = 0; i < lines_parsed.length; i++) {
                        lines.add(lines_parsed[i]);
                    };
                };
            })
            .fail(function(e) {
                alert('error in retrieve')
                console.log(e);
            });
            
        }

    });

    var App = new Edits;

    function drawLine(ctx, x1, y1, x2, y2, hover){
        ctx.strokeWidth = 3;
        if(hover){
            ctx.strokeStyle = '#FFDC00';
        }else{
            ctx.strokeStyle = '#001F3F';
        };
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
    }

    function drawCircle(ctx, x, y){
        ctx.fillStyle = '#0074D9';
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI, true);
        ctx.fill();
    }

    function clearCxt(ctx){
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }

    function drawAllLines(ctx, lines){
        clearCxt(ctx);
        lines.each(function(line){
            drawLine(ctx, line.get('x1'), line.get('y1'), line.get('x2'), line.get('y2'), line.get('hover'));
        });
    }
});


