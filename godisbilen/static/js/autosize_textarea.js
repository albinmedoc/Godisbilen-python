class AutosizeTextarea{
    constructor(textarea){
        this.textarea = textarea;
        var events = [["change", this.resize], ["cut", this.delayedResize], ["paste", this.delayedResize], ["drop", this.delayedResize], ["keydown", this.delayedResize]];
        for(event in events){
            if (window.attachEvent){
                this.textarea.attachEvent("on"+events[event][0], events[event][1].bind(null, this));
            }else{
                this.textarea.addEventListener(events[event][0], events[event][1].bind(null, this), false);
            }
        }
        this.resize(this);
    }

    resize(autosize){
        var clone = autosize.textarea.cloneNode();
        clone.className = "clone";
        clone.style.position = "absolute";
        clone.style.visibility = "hidden";
        autosize.textarea.parentNode.insertBefore(clone, autosize.textarea);
        clone.style.height = "auto";
        clone.value = autosize.textarea.value;
        autosize.textarea.style.height = (clone.scrollTop + clone.scrollHeight + 20) + "px";
        autosize.textarea.parentNode.removeChild(clone);
    }

    delayedResize(autosize){
        window.setTimeout(autosize.resize.bind(null, autosize), 0);
    }
}