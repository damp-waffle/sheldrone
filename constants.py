auth_token_disclaimer = (
            "In order to register you, I will save your Discord User ID to my database and pair it to a Nintendo Switch Online session token. If you aren't aware of Nintendo's use of authentication tokens, "
            + "please read the notice below before proceeding:\n\n"
            + "```This bot allows for automatic token generation. Automatic token generation involves making a secure request to a non-Nintendo server with minimal, non-identifying information. "
            + "The server used for token generation is the nxapi-znca-api, an API used by the popular tool/app nxapi and many other applications such as this one to generate authentication tokens for the NSO App API. "
            + "For transparency and in accordance with the usage terms of nxapi-znca-api, the end user help guide is linked below. Any issues with Shel-drone should not be directed to the creator of nxapi. "
            + "Users who feel uncomfortable with this process may opt to manually retrieve and input their tokens instead. For information on manually retrieving your NSO tokens, refer to the Token Generation "
            + "section of the s3s github page (https://github.com/frozenpandaman/s3s?tab=readme-ov-file#token-generation-)\n\nIf you already use s3s, you can copy the session_token from your config.txt file "
            + "in the s3s directory. Whatever method you opt for, make absolutely sure that you do NOT share your session token with anyone else. If you do, they will have access to your Nintendo Switch Online "
            + "account and will be able to make requests on your behalf. If you are concerned about your session token being leaked, you can revoke it.```\n"
            + "Unfortunately, if you feel uncomfortable with Shel-drone's requirement of storing your Discord User ID and NSO authentication tokens, there is no other solution as of right now that "
            + "allows for the bot's functionality in a more secure or efficient way. If there is demand for such a solution, then one will be looked into. But there are no plans to do so at this time."
            + "\n\n Are you ready to continue?\n")

auto_sesh_instr = (
            "1. Navigate to [this URL]({0}) in your browser by either following the link [here]({0}), clicking on the button below, or by pasting this into your browser:```{0}```\n"
            + "2. Log into your Nintendo account\n"
            + "3. Right-click on the red **\"Select this account\"** button and select **\"Copy link address\"**.\n"
            + "4. Paste the URL you just copied below and send it within 5 minutes. (The message you send it in will be deleted for privacy. The message will be verified for following the correct format and session before it accepts it, so don't worry if you paste the wrong thing.)"
)

token_rec="Running any command that fetches information from Splatnet can regenerate your tokens. As long as the session token is valid, your g token and bullet token will automatically regenerate each time you use a command that requires them."

questionmark = '<:unknown:1350552391833092159>'
loadinganimation = '<a:loading:1370229081794416670>'


modeColor= {
           'PRIVATE'  :0xa51ee1,
           'REGULAR'  :0xcff662,
           'BANKARA'  :0xf54910,
           'X_BATTLE' :0x0fdb9b,
           'LEAGUE'   :0xf02d7d,
           'FEST'     :0xffffff}
modeMoji = {
           'PRIVATE'  :'<:pb:1350543221075218512>',
           'REGULAR'  :'<:tw:1350543386268008653>',
           'BANKARA'  :'<:ab:1350543025021124669>',
           'X_BATTLE' :'<:xb:1350543097158697102>',
           'LEAGUE'   :'<:ch:1350543131807842386>',
           'FEST'     :'<:sf:1350543336305590272>',
           '?'        :questionmark}
ruleMoji = {
           'A':'<:tw:1350543386268008653>',
           'E':'<:sz:1350542653573435392>',
           'I':'<:tc:1350542722980642977>',
           'M':'<:rm:1350542749866262618>',
           'Q':'<:cb:1350542772075106466>',
           'U':'<:tri:1350543360020058184>',
           '?':questionmark}

REPLAY_URL = 'https://s.nintendo.com/av5ja-lp1/znca/game/4834290508791808?p=%2Freplay%3Fcode%3D'

SPLATNET_URL = "https://api.lp1.av5ja.srv.nintendo.net"

SPLATNET_VERSION = "2.12.0"

SPLATOON_VERSION = "9.3.0"

medals = {
    "#1 Overall Splatter":"<:gold:1350542957194776666>",
    "#1 Splat Zone Inker":"<:gold:1350542957194776666>",
    "#1 Splat Zone Guard":"<:gold:1350542957194776666>",
    "#1 Score Booster":"<:gold:1350542957194776666>",
    "Record-Score Setter":"<:gold:1350542957194776666>",
    "#1 Clam Carrier":"<:gold:1350542957194776666>",
    "#1 Turf Inker":"<:gold:1350542957194776666>",
    "#1 Popular Target":"<:gold:1350542957194776666>",
    "#1 Home-Base Inker":"<:gold:1350542957194776666>",
    "#1 Enemy-Base Inker":"<:gold:1350542957194776666>",
    "#1 Super Jump Spot":"<:gold:1350542957194776666>",
    "#1 Enemy Splatter":"<:gold:1350542957194776666>",
    "#1 Splat Assister":"<:gold:1350542957194776666>",
    "#1 Splat Zone Hero":"<:silver:1350542991554515016>",
    "#1 Checkpoint Breaker":"<:silver:1350542991554515016>",
    "#1 Tower Stopper":"<:silver:1350542991554515016>",
    "#1 Rainmaker Carrier":"<:silver:1350542991554515016>",
    "#1 Rainmaker Stopper":"<:silver:1350542991554515016>",
    "#1 Clam Stopper":"<:silver:1350542991554515016>",
    "#1 Base Defender":"<:silver:1350542991554515016>",
    "#1 Ground Traveler":"<:silver:1350542991554515016>",
    "#1 Damage Taker":"<:silver:1350542991554515016>",
    "#1 Ink Consumer":"<:silver:1350542991554515016>",
    "First Splat!":"<:silver:1350542991554515016>",
    "#1 Trizooka User":"<:silver:1350542991554515016>",
    "#1 Big Bubbler User":"<:silver:1350542991554515016>",
    "#1 Killer Wail 5.1 User":"<:silver:1350542991554515016>",
    "#1 Tenta Missiles User":"<:silver:1350542991554515016>",
    "#1 Ink Storm User":"<:silver:1350542991554515016>",
    "#1 Booyah Bomb User":"<:silver:1350542991554515016>",
    "#1 Ultra Stamp User":"<:silver:1350542991554515016>",
    "#1 Inkjet User":"<:silver:1350542991554515016>",
    "#1 Zipcaster User":"<:silver:1350542991554515016>",
    "#1 Wave Breaker User":"<:silver:1350542991554515016>",
    "#1 Ink Vac User":"<:silver:1350542991554515016>",
    "#1 Crab Tank User":"<:silver:1350542991554515016>",
    "#1 Reefslider User":"<:silver:1350542991554515016>",
    "#1 Triple Inkstrike User":"<:silver:1350542991554515016>",
    "#1 Tacticooler User":"<:silver:1350542991554515016>",
    "#1 Kraken Royale User":"<:silver:1350542991554515016>",
    "#1 Super Chump User":"<:silver:1350542991554515016>",
    "#1 Triple Splashdown User":"<:silver:1350542991554515016>",
    "#1 Splattercolor Screen User":"<:silver:1350542991554515016>",
    "#2 Overall Splatter":"<:silver:1350542991554515016>",
    "#2 Splat Zone Inker":"<:silver:1350542991554515016>",
    "#2 Splat Zone Guard":"<:silver:1350542991554515016>",
    "#2 Score Booster":"<:silver:1350542991554515016>",
    "#2 Clam Carrier":"<:silver:1350542991554515016>",
    "#2 Turf Inker":"<:silver:1350542991554515016>",
    "#2 Popular Target":"<:silver:1350542991554515016>",
    "#2 Home-Base Inker":"<:silver:1350542991554515016>",
    "#2 Enemy-Base Inker":"<:silver:1350542991554515016>",
    "#2 Super Jump Spot":"<:silver:1350542991554515016>",
    "#2 Enemy Splatter":"<:silver:1350542991554515016>",
    "#2 Splat Assister":"<:silver:1350542991554515016>"
}

sha_keys = {
    "SupportButton_SupportChallengeMutation": "3165b76878d09ea55a7194e675397a5e030a2a89b98a0e81af77e346c625c4fd",
    "CheckinWithQRCodeMutation": "63a60eea7926b0f2600cfb64d8bf3b6736afc1e1040beabd5dfa40fbfdcb92d8",
    "CoopPagerLatestCoopQuery": "bc8a3d48e91d5d695ef52d52ae466920670d4f4381cb288cd570dc8160250457",
    "RankingHoldersFestTeamRankingHoldersPaginationQuery": "34460535ce2b699ed0617d67e22a7e3290fd30041559bf6f05d408d06f1c9938",
    "VotesUpdateFestVoteMutation": "b0830a3c3c9d8aa6ed83e200aed6b008f992acdba4550ab4399417c1f765e7e3",
    "CreateMyOutfitMutation": "b5257c5a3840cb01556750cbb56881d758534dfd91e9aec7c0232098fd767bb9",
    "UpdateMyOutfitMutation": "b83ed5a9b58252c088d3aac7f28a34a59acfbaa61b187ee3eebfe8506aa720f9",
    "DownloadSearchReplayQuery": "2805ee5182dd44c5114a1e6cfa57b2bcbbe9173c7e52069cc85a518de49c2191",
    "ReplayModalReserveReplayDownloadMutation": "07e94ba8076b235d9b16c9e8d1714dfffbd4441c17225c36058b8a7ba44458b1",
    "PagerLatestVsDetailQuery": "73462e18d464acfdf7ac36bde08a1859aa2872a90ed0baed69c94864c20de046",
    "PagerUpdateBattleHistoriesByVsModeQuery": "ac6561ff575363efcc9b876cf179929203dab17d3f25ab293a1123f4637e1dc7",
    "ConfigureAnalyticsQuery": "2a9302bdd09a13f8b344642d4ed483b9464f20889ac17401e993dfa5c2bb3607",
    "useCurrentFestQuery": "980af9d079ce2a6fa63893d2cd1917b70a229a222b24bbf8201f48d814ff48f0",
    "useShareMyOutfitQuery": "5502b09121f5e18bec8fefbe80cce21e1641624b579c57c1992b30dcff612b44",
    "BankaraBattleHistoriesQuery": "9863ea4744730743268e2940396e21b891104ed40e2286789f05100b45a0b0fd",
    "BankaraBattleHistoriesRefetchQuery": "7673fe37d5d5d81fa37d0b1cc02cffd7453a809ecc76b000c67d61aa51a39890",
    "EventBattleHistoriesQuery": "e47f9aac5599f75c842335ef0ab8f4c640e8bf2afe588a3b1d4b480ee79198ac",
    "EventBattleHistoriesRefetchQuery": "a30281d08421b916902e4972f0d48d4d3346a92a68cbadcdb58b4e1a06273296",
    "LatestBattleHistoriesQuery": "b24d22fd6cb251c515c2b90044039698aa27bc1fab15801d83014d919cd45780",
    "LatestBattleHistoriesRefetchQuery": "58bf17200ca97b55d37165d44902067b617d635e9c8e08e6721b97e9421a8b67",
    "PrivateBattleHistoriesQuery": "fef94f39b9eeac6b2fac4de43bc0442c16a9f2df95f4d367dd8a79d7c5ed5ce7",
    "PrivateBattleHistoriesRefetchQuery": "3dd1b491b2b563e9dfc613e01f0b8e977e122d901bc17466743a82b7c0e6c33a",
    "RegularBattleHistoriesQuery": "2fe6ea7a2de1d6a888b7bd3dbeb6acc8e3246f055ca39b80c4531bbcd0727bba",
    "RegularBattleHistoriesRefetchQuery": "e818519b50e877ac6aeaeaf19e0695356f28002ad4ccf77c1c4867ef0df9a6d7",
    "XBattleHistoriesQuery": "eb5996a12705c2e94813a62e05c0dc419aad2811b8d49d53e5732290105559cb",
    "XBattleHistoriesRefetchQuery": "a175dc519f551c0bbeed04286194dc12b1a05e3117ab73f6743e5799e91f903a",
    "BattleHistoryCurrentPlayerQuery": "8b59e806751e4e74359b416472925bb405601a626743084d2158af72cc3e7716",
    "ChallengeQuery": "65252c7bbca148daf34de9a884e651bf9a5c1880a23f3d1e175a33f146b9f6dc",
    "ChallengeRefetchQuery": "636c7f8180469847bbfe005afb589ee041bc8ca653c2a26d07987e582179fcad",
    "JourneyChallengeDetailQuery": "ed634e52cd478ebc9d77d84831665aabfac14ac74bb343aa73c310539894169a",
    "JourneyChallengeDetailRefetchQuery": "c7e4044cc4320e4ae44ccda1b7eb74897d213628c4e5d2f2863df5f8e8a9478d",
    "JourneyQuery": "c0cd04d2f0b00444853bae0d7e7f1ac534dfd7ff593c738ab9ba4456b1e85f8a",
    "JourneyRefetchQuery": "d5fc5dd3a144139e89815b9e3af6499f58e5fc5185876840dd6edadb0ca214b4",
    "CheckinQuery": "6dfce83d02761395758ae21454cb46924e81c22c3f151f91330b0602278a060e",
    "CoopHistoryDetailQuery": "824a1e22c4ad4eece7ad94a9a0343ecd76784be4f77d8f6f563c165afc8cf602",
    "CoopHistoryDetailRefetchQuery": "4bf516ccfd9a3f4efc32b215c59ae42c2a06dd2d8f73de95c2676dea6db74446",
    "CoopHistoryQuery": "0f8c33970a425683bb1bdecca50a0ca4fb3c3641c0b2a1237aedfde9c0cb2b8f",
    "refetchableCoopHistory_coopResultQuery": "bdb796803793ada1ee2ea28e2034a31f5c231448e80f5c992e94b021807f40f8",
    "CoopRecordBigRunRecordContainerPaginationQuery": "4e357d607d98fa3b0f919f3aa0061af717c55c16017e31040647159bdb14601b",
    "CoopRecordQuery": "940418e7b67b69420b7af50bdd292639e46fa8240ae57520a9cf7eed05a10760",
    "CoopRecordRefetchQuery": "563536def9d127eb5c66eef94f9f3e10e5af00b0be6b8faa1692ae259e023fb3",
    "EventMatchRankingPeriodQuery": "ad4097d5fb900b01f12dffcb02228ef6c20ddbfba41f0158bb91e845335c708e",
    "EventMatchRankingQuery": "875a827a6e460c3cd6b1921e6a0872d8b95a1fce6d52af79df67734c5cc8b527",
    "EventMatchRankingRefetchQuery": "e9af725879a454fd3d5a191862ec3a544f552ae2d9bff6de6b212ac2676e8e14",
    "EventMatchRankingSeasonRefetchQuery": "5b563e5fb86ff7e537cc1ed86485049a41a710ca79af9c38113d41dda1d54643",
    "DetailFestRecordDetailQuery": "02946c9d6dec617425ed41ee9a9bf467ea2ddfb85e0a36b09e4c3ea2e0b9ac5b",
    "DetailFestRefethQuery": "dc5c1890cec78094d919e71621e9b4bc1ee06cfa99812dcacb401b8116a1ccad",
    "DetailFestVotingStatusRefethQuery": "4a24f9ff7b1c5a5c520872ce083c1623354c3ec092a0bf95c0dc1c12a1e3fb63",
    "DetailRankingQuery": "2e1f603f6da371874a7473bb68418d9308f1fd2492e57fd2b7d9bbb80138f8c0",
    "DetailVotingStatusQuery": "e2aafab18dab26ba1b6d40838c6842201f6480d62f8f3dffecad8dd4c5b102c1",
    "FestRecordQuery": "c8660a636e73dcbf55c12932bc301b1c9db2aa9a78939ff61bf77a0ea8ff0a88",
    "FestRecordRefetchQuery": "87ed3300bdecdb51090398d43ee0957e69b7bd1370ac38d03f6c7cb160b4586a",
    "FriendListQuery": "ea1297e9bb8e52404f52d89ac821e1d73b726ceef2fd9cc8d6b38ab253428fb3",
    "FriendListRefetchQuery": "411b3fa70a9e0ff083d004b06cc6fad2638a1a24326cbd1fb111e7c72a529931",
    "GesotownQuery": "d6f94d4c05a111957bcd65f8649d628b02bf32d81f26f1d5b56eaef438e55bab",
    "GesotownRefetchQuery": "681841689c2d0f8d3355b71918d6c9aedf68484dfcb06b144407df1c4873dea0",
    "SaleGearDetailOrderGesotownGearMutation": "bb716c3be6e85331741d7e2f9b36a6c0de92ca1b8382418744c1540fec7c8f57",
    "SaleGearDetailQuery": "b42e70a6873aa716d089f2c5ea219083d30f0fff6ed15b8f5630c01ef7a32015",
    "HeroHistoryQuery": "71019ce4389463d9e2a71632e111eb453ca528f4f794aefd861dff23d9c18147",
    "HeroHistoryRefetchQuery": "c6cb0b7cfd8721e90e3a85d3340d190c7f9c759b6b5e627900f5456fec61f6ff",
    "HistoryRecordQuery": "0a62c0152f27c4218cf6c87523377521c2cff76a4ef0373f2da3300079bf0388",
    "HistoryRecordRefetchQuery": "a5d80de05d1d4bfce67a1fb0801495d8bc6bba6fd780341cb90ddfeb1249c986",
    "MyOutfitDetailQuery": "e2c9ea77f0469cb8109c54e93f3f35c930dfeb5b79cbf639397828a805ad9248",
    "MyOutfitsQuery": "5b32bb88c47222522d2bc3643b92759644f890a70189a0884ea2d456a8989342",
    "MyOutfitsRefetchQuery": "565bc1f16c0a5088d41b203775987c70756296747ba905c3e1c0ce8f3f27f925",
    "myOutfitCommonDataEquipmentsQuery": "45a4c343d973864f7bb9e9efac404182be1d48cf2181619505e9b7cd3b56a6e8",
    "myOutfitCommonDataFilteringConditionQuery": "ac20c44a952131cb0c9d00eda7bc1a84c1a99546f0f1fc170212d5a6bb51a426",
    "PhotoAlbumQuery": "62383a0595fab69bf49a2a6877bc47acc081bfa065cb2eae28aa881980bb30b2",
    "PhotoAlbumRefetchQuery": "0819c222d0b68fbcc7706f60b98e797da7d1fce637b45b3bdadca1ccdb692c86",
    "ReplayQuery": "3af48164d1176e8a88fb5321f5fb2daf9dde00b314170f1848a30e1825fc828e",
    "ReplayUploadedReplayListRefetchQuery": "1e42b2238c385b5db29717b98d0df5934c75e8807545091d97200127ed1ecef0",
    "SettingQuery": "8473b5eb2c2048f74eb48b0d3e9779f44febcf3477479625b4dc23449940206b",
    "StageRecordQuery": "c8b31c491355b4d889306a22bd9003ac68f8ce31b2d5345017cdd30a2c8056f3",
    "StageRecordsRefetchQuery": "25dbf592793a590b6f8cfb0a62823aa02429b406a590333627d8ea703b190dfd",
    "StageScheduleQuery": "9b6b90568f990b2a14f04c25dd6eb53b35cc12ac815db85ececfccee64215edd",
    "WeaponRecordQuery": "974fad8a1275b415c3386aa212b07eddc3f6582686e4fef286ec4043cdf17135",
    "WeaponRecordsRefetchQuery": "7d7194a98cb7b0b235f15f98a622fab4945992fd268101e24443db82569dd25d",
    "DetailTabViewWeaponTopsArRefetchQuery": "0d97601d58e0eba18ea83fcce9789e35e10413344ccda7f9bb83129a2d7949f4",
    "DetailTabViewWeaponTopsClRefetchQuery": "42baca97f8038f51ffedc9bf837e820797d31c80cf4bac9b5b400fddb37ff3e1",
    "DetailTabViewWeaponTopsGlRefetchQuery": "a5237b76a33b7ee3eb79a2fe83f297e0e1324a3bf42bea9182ea49a5396bb053",
    "DetailTabViewWeaponTopsLfRefetchQuery": "2d23e55747f5365466b9563a89acb21851894b384fdbd33c80f8ee192b3d825b",
    "DetailTabViewXRankingArRefetchQuery": "0dc7b908c6d7ad925157a7fa60915523dab4613e6902f8b3359ae96be1ba175f",
    "DetailTabViewXRankingClRefetchQuery": "485e5decc718feeccf6dffddfe572455198fdd373c639d68744ee81507df1a48",
    "DetailTabViewXRankingGlRefetchQuery": "6ab0299d827378d2cae1e608d349168cd4db21dd11164c542d405ed689c9f622",
    "DetailTabViewXRankingLfRefetchQuery": "ca55206629f2c9fab38d74e49dda3c5452a83dd02a5a7612a2520a1fc77ae228",
    "XRankingDetailQuery": "90932ee3357eadab30eb11e9d6b4fe52d6b35fde91b5c6fd92ba4d6159ea1cb7",
    "XRankingDetailRefetchQuery": "00e8e962cc65795c6480d10caddaee7e0262d5cdf81e5958ff8f3359bd2f9743",
    "XRankingQuery": "a5331ed228dbf2e904168efe166964e2be2b00460c578eee49fc0bc58b4b899c",
    "XRankingRefetchQuery": "5a469004feb402a1d44a10820b647def2d4eb320436f6add4431194a34d0b497",
    "CatalogQuery": "40b62e4734f22a6009f1951fc1d03366b14a70833cb96a9a46c0e9b7043c67ef",
    "CatalogRefetchQuery": "c4f5474dfc5d7937618d8a38357ad1e78cc83d6019833b1b68d86a0ce8d4b9e5",
    "HomeQuery": "51fc56bbf006caf37728914aa8bc0e2c86a80cf195b4d4027d6822a3623098a8",
    "VsHistoryDetailPagerRefetchQuery": "973ca7012d8e94da97506cd39dfbb2a45eaae6e382607b650533d4f5077d840d",
    "VsHistoryDetailQuery": "f893e1ddcfb8a4fd645fd75ced173f18b2750e5cfba41d2669b9814f6ceaec46"
 }

helpText1 = {
    'title':'Replay Commands',
    'description':'**Notes:**\n- Replay Codes will automatically have invalid alphanumeric characters replaced with the correct versions. This means \'IOZ\' becomes \'102\'.'
    +'\n- The download queue buttons work as long as the bot is running, no matter if the message has timed out. For batches, this requires the use of a file attachment present in the messages in which they are displayed.',
    'fields':[
        {
            'name':'``/getreplay [replay_code]``',
            'value':'Loads replay data from a provided `replay_code`. Displays the replay data in an Embed, along with a button to queue the replay to be downloaded in the Splatoon 3 lobby.\n'
        },
        {
            'name':'``/getrecentreplays``\n``/getrecentreplays [number]``',
            'value':'Loads the replay data of up to 30 of the user\'s most recently uploaded replays. A `number` of replays to grab can be specified, but does 30 by default.'
            + ' Displays the replay data in an Embed, along with a button to queue the batch to be downloaded in the Splatoon 3 lobby. A batch file is included in the message to assist the button\'s functionality.\n'
        },
        {
            'name':'``/getbatch [replay_code] [replay_code]...``\n``/getbatch "[title]" [replay_code]...``',
            'value':'Loads the replay data of up to 30 different replays from provided space-separated `replay_code`s. Optionally, a `title` for the replay batch can be provided *before* the `replay_code`s, if surrounded by quotation marks (`"`).'
            + ' Displays the replay data in an Embed, along with a button to queue the batch to be downloaded in the Splatoon 3 lobby. A batch file is included in the message to assist the button\'s functionality.\n'
        }
    ]
}
helpText2 = {
    'title':'Token Commands',
    'description':'',
    'fields':[
        {
            'name':'``/register``',
            'value':'Registers a user to the bot. This requires storing their session token and tying it to their Discord User ID in the bot\'s database.'
        },
        {
            'name':'``/newtoken``',
            'value':'Updates a user\'s session token in the bot\'s database. This overwrites the currently stored session token with a new one.'
        },
        {
            'name':'``/tokenstatus``',
            'value':'Displays info about the user\'s tokens, specifically: validity, when they were generated, and how long until they expire. Displays this info ephemerally (viewable only by the user) and does not attempt to update or refresh tokens.'
        }
    ]
}
helpText3 = {
    'title':'Other Commands',
    'description':'',
    'fields':[
        {
            'name':'``/getalbum``\n``/getalbum [number]``',
            'value':'Loads and sends all recently uploaded photos from the user\'s Splatnet3 album. A `number` of photos to grab can be specified, if not all available photos will be fetched. Note: only four images can be sent per message.'
        }
    ]
}