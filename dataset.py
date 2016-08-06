dataList = {
    "thbgm" : {
        "name" : "thbgm"
        ,"directory" : "./data/thbgm/*/*.mp3"
    }
    ,"not_thbgm" : {
        "name" : "not_thbgm"
        ,"directory" : "./data/not_thbgm/*/*.mp3"
    }
    ,"thbgm_test" : {
        "name" : "thbgm_test"
        ,"directory" : "./data/thbgm_test/*/*.mp3"
    }
    ,"gtzan" : {
        "name" : "gtzan"
        ,"directory" : "./data/gtzan/*/*.au"
    }
    ,"anison" : {
        "name" : "anison"
        ,"directory" : "./data/anison/*/*.mp3"
    }
    ,"magna" : {
        "name" : "magna"
        ,"directory" : "./data/magna/*/*.mp3"
    }
}

trainDataTrue = ["thbgm"]
trainDataFalse = ["not_thbgm"]
testData = ["thbgm_test","gtzan","anison","magna"]
allData = trainDataTrue+trainDataFalse+testData
