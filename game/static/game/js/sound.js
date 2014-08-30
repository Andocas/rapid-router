var ocargo = ocargo || {};

ocargo.sound = {};

ocargo.sound.startingSound = new Howl({
    urls: ['/static/game/sound/starting.mp3', '/static/game/sound/starting.ogg']
});

ocargo.sound.engineSound = new Howl({
    urls: ['/static/game/sound/moving.mp3', '/static/game/sound/moving.ogg'],
    loop: true
});

ocargo.sound.deliverySound = new Howl({
    urls: ['/static/game/sound/delivery.mp3', '/static/game/sound/delivery.ogg']
});

ocargo.sound.winSound = new Howl({
    urls: ['/static/game/sound/win.mp3', '/static/game/sound/win.ogg']
});

ocargo.sound.failureSound = new Howl({
    urls: ['/static/game/sound/failure.mp3', '/static/game/sound/failure.ogg']
});

ocargo.sound.crashSound = new Howl({
    urls: ['/static/game/sound/crash.mp3', '/static/game/sound/crash.ogg']
});

ocargo.sound.tensionSound = new Howl({
    urls: ['/static/game/sound/tension.mp3', '/static/game/sound/tension.ogg']
});

function safePlay(sound) {
    try {
        sound.play();
    }
    catch (err) {}
}

function safeStop(sound) {
    try {
        sound.stop();
    }
    catch (err) {}
}


ocargo.sound.starting = function() {
    if (CHARACTER_NAME === 'Van') {
        safePlay(ocargo.sound.startingSound);
    }
};

ocargo.sound.start_engine = function() {
    if (CHARACTER_NAME === 'Van') {
        safePlay(ocargo.sound.engineSound);
    }
};

ocargo.sound.stop_engine = function() {
    if (CHARACTER_NAME === 'Van') {
        safeStop(ocargo.sound.engineSound);
    }
};

ocargo.sound.delivery = function() {
    safePlay(ocargo.sound.deliverySound);
};

ocargo.sound.win = function() {
    safePlay(ocargo.sound.winSound);
};

ocargo.sound.failure = function() {
    safePlay(ocargo.sound.failureSound);
};

ocargo.sound.crash = function() {
    if (CHARACTER_NAME === 'Van') {
        safePlay(ocargo.sound.crashSound);
    } else {
        safePlay(ocargo.sound.failureSound);
    }
};

ocargo.sound.tension = function() {
    safePlay(ocargo.sound.tensionSound);
};

ocargo.sound.mute = function() {
    this.playAudioBackup = Blockly.SOUNDS_;
    Blockly.SOUNDS_ = {};
    
    Howler.mute();
};

ocargo.sound.unmute = function() {
    Blockly.SOUNDS_ = this.playAudioBackup || Blockly.SOUNDS_;

    Howler.unmute();
};
