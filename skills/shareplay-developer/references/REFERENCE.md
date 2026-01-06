# SharePlay Example Code References

## Notes
- Sources: Apple sample "Building a Guessing Game for visionOS" (GuessTogether); Apple sample "Drawing Content in a Group Session" (DrawTogether).
- Scope: Only files that directly use GroupActivities APIs (GroupActivity, GroupSession, GroupStateObserver, GroupSessionMessenger/Journal, SpatialTemplate, Participant).
- Non-GroupActivities UI, assets, and JSON files are omitted.
- See the original samples' LICENSE.txt files for licensing terms.

## Table of Contents
- [Skill patterns (GroupActivities)](#skill-patterns-groupactivities)
  - [Define a GroupActivity with Transferable metadata](#define-a-groupactivity-with-transferable-metadata)
  - [Activate and observe sessions](#activate-and-observe-sessions)
  - [Synchronize state with messenger and journal](#synchronize-state-with-messenger-and-journal)
- [Guess Together sample (GroupActivities)](#guess-together-sample-groupactivities)
  - [GuessTogether.entitlements](#guesstogetherentitlements)
  - [GuessTogetherActivity.swift](#guesstogetheractivityswift)
  - [MainView.swift](#mainviewswift)
  - [SharePlayButton.swift](#shareplaybuttonswift)
  - [GameModel.swift](#gamemodelswift)
  - [SessionController.swift](#sessioncontrollerswift)
  - [SessionController+PlayerOrder.swift](#sessioncontrollerplayerorderswift)
  - [SessionController+RemoteParticipantSynchronization.swift](#sessioncontrollerremoteparticipantsynchronizationswift)
  - [GameTemplate.swift](#gametemplateswift)
  - [TeamSelectionTemplate.swift](#teamselectiontemplateswift)
- [Draw Together sample (GroupActivities)](#draw-together-sample-groupactivities)
  - [DrawTogether.entitlements](#drawtogetherentitlements)
  - [DrawTogether.swift](#drawtogetherswift)
  - [ContentView.swift](#contentviewswift)
  - [ControlBar.swift](#controlbarswift)
  - [Canvas.swift](#canvasswift)
  - [Messages.swift](#messagesswift)

## Skill patterns (GroupActivities)

These patterns are synthesized examples to illustrate common GroupActivities flows.

### Define a GroupActivity with Transferable metadata

```swift
import CoreTransferable
import Foundation
import GroupActivities

struct Movie: Codable, Transferable {
    let title: String
    let url: URL

    static var transferRepresentation: some TransferRepresentation {
        ProxyRepresentation(exporting: \.url)
        GroupActivityTransferRepresentation { movie in
            WatchTogether(movie: movie)
        }
    }
}

struct WatchTogether: GroupActivity {
    static let activityIdentifier = "com.example.app.watch-together"

    let movie: Movie

    var metadata: GroupActivityMetadata {
        var metadata = GroupActivityMetadata()
        metadata.type = .watchTogether
        metadata.title = movie.title
        metadata.fallbackURL = movie.url
        metadata.supportsContinuationOnTV = true
        return metadata
    }
}
```

### Activate and observe sessions

```swift
import GroupActivities

@MainActor
func startSharePlay(activity: WatchTogether, groupState: GroupStateObserver) async {
    if groupState.isEligibleForGroupSession {
        switch await activity.prepareForActivation() {
        case .activationPreferred:
            _ = try? await activity.activate()
        case .activationDisabled, .cancelled:
            break
        @unknown default:
            break
        }
    } else {
        // Present GroupActivitySharingController or a ShareLink-based share sheet.
    }
}

@MainActor
func observeSessions() {
    Task {
        for await session in WatchTogether.sessions() {
            await configure(session)
        }
    }
}

@MainActor
func configure(_ session: GroupSession<WatchTogether>) async {
    if let coordinator = await session.systemCoordinator {
        var config = SystemCoordinator.Configuration()
        config.spatialTemplatePreference = .sideBySide
        config.supportsGroupImmersiveSpace = true
        coordinator.configuration = config
    }
    session.join()
}
```

### Synchronize state with messenger and journal

```swift
import CoreGraphics
import Foundation
import GroupActivities

struct StrokeMessage: Codable, CustomMessageIdentifiable {
    static let messageIdentifier = "com.example.app.stroke"
    let id: UUID
    let point: CGPoint
}

final class SessionSync {
    private let session: GroupSession<WatchTogether>
    private let messenger: GroupSessionMessenger
    private let journal: GroupSessionJournal

    init(session: GroupSession<WatchTogether>) {
        self.session = session
        self.messenger = GroupSessionMessenger(session: session, deliveryMode: .reliable)
        self.journal = GroupSessionJournal(session: session)
    }

    func startListening() {
        Task {
            for await (message, _) in messenger.messages(of: StrokeMessage.self) {
                handle(message)
            }
        }
    }

    func send(_ message: StrokeMessage) async {
        try? await messenger.send(message, to: .all)
    }

    func listenForAttachments() {
        Task {
            for await attachments in journal.attachments {
                for attachment in attachments {
                    _ = try? await attachment.load(Data.self)
                }
            }
        }
    }

    private func handle(_ message: StrokeMessage) {
        // Update local state from the incoming message.
    }
}
```

## Guess Together sample (GroupActivities)

Source root: `BuildingAGuessingGameForVisionOS/GuessTogether`

### GuessTogether.entitlements
Path: `GuessTogether/Resources/GuessTogether.entitlements`

```entitlements
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>com.apple.developer.group-session</key>
	<true/>
</dict>
</plist>
```

### GuessTogetherActivity.swift
Path: `GuessTogether/GroupActivity/GuessTogetherActivity.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The implementation of the Guess Together app's group activity.
*/

import CoreTransferable
import GroupActivities

struct GuessTogetherActivity: GroupActivity, Transferable, Sendable {
    var metadata: GroupActivityMetadata = {
        var metadata = GroupActivityMetadata()
        metadata.title = "Guess Together"
        return metadata
    }()
}
```

### MainView.swift
Path: `GuessTogether/WindowViews/MainView.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The main UI view, which presents different subviews based on the app's current state.
*/

import GroupActivities
import SwiftUI

/// A top-level content view that presents the app's user interface based on
/// the app's current stage.
///
/// Guess Together has four stages:
///
/// 1. A welcome stage that is presented when you first launch the app and
///    invites you to create a SharePlay group session with your current
///    FaceTime call.
///
/// 2. A category selection stage where you'll decide what categories you want
///    to play with. For example, maybe you want to play with phrases pulled
///    from historical events, or with something more simple, like different
///    fruits and vegetables.
///
/// 3. A team selection stage where you'll decide to join the Blue or Red team.
///
/// 4. A game stage where Guess Together will open an immersive space and
///    present a view with a scoreboard and a timer. An additional view appears
///    in front of the active player with the secret phrase their teammates will
///     need to guess.
struct MainView: View {
    @Environment(AppModel.self) var appModel
    
    var body: some View {
        Group {
            // Select the appropriate view for each stage in the game.
            switch appModel.sessionController?.game.stage {
                case .none:
                    WelcomeView()
                case .categorySelection:
                    CategorySelectionView()
                case .teamSelection:
                    TeamSelectionView()
                case .inGame:
                    ScoreBoardView()
            }
        }
        .task(observeGroupSessions)
    }
    
    /// Monitor for new Guess Together group activity sessions.
    @Sendable
    func observeGroupSessions() async {
        for await session in GuessTogetherActivity.sessions() {
            let sessionController = await SessionController(session, appModel: appModel)
            guard let sessionController else {
                continue
            }
            appModel.sessionController = sessionController

            // Create a task to observe the group session state and clear the
            // session controller when the group session invalidates.
            Task {
                for await state in session.$state.values {
                    guard appModel.sessionController?.session.id == session.id else {
                        return
                    }

                    if case .invalidated = state {
                        appModel.sessionController = nil
                        return
                    }
                }
            }
        }
    }
}
```

### SharePlayButton.swift
Path: `GuessTogether/WindowViews/Shared/SharePlayButton.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The implementation of the SharePlay button.
*/

import CoreTransferable
import GroupActivities
import SwiftUI
import UIKit

struct SharePlayButton<ActivityType: GroupActivity & Transferable & Sendable>: View {
    @ObservedObject
    private var groupStateObserver = GroupStateObserver()
    
    @State
    private var isActivitySharingViewPresented = false
    
    @State
    private var isActivationErrorViewPresented = false
    
    private let activitySharingView: ActivitySharingView<ActivityType>
    
    let text: any StringProtocol
    let activity: ActivityType
    
    init(_ text: any StringProtocol, activity: ActivityType) {
        self.text = text
        self.activity = activity
        self.activitySharingView = ActivitySharingView {
            activity
        }
    }
    
    var body: some View {
        ZStack {
            ShareLink(item: activity, preview: SharePreview(text)).hidden()
            
            Button(text, systemImage: "shareplay") {
                if groupStateObserver.isEligibleForGroupSession {
                    Task.detached {
                        do {
                            _ = try await activity.activate()
                        } catch {
                            print("Error activating activity: \(error)")
                            
                            Task { @MainActor in
                                isActivationErrorViewPresented = true
                            }
                        }
                    }
                } else {
                    isActivitySharingViewPresented = true
                }
            }
            .tint(.green)
            .sheet(isPresented: $isActivitySharingViewPresented) {
                activitySharingView
            }
            .alert("Unable to start game", isPresented: $isActivationErrorViewPresented) {
                Button("Ok", role: .cancel) { }
            } message: {
                Text("Please try again later.")
            }
        }
    }
}

struct ActivitySharingView<ActivityType: GroupActivity & Sendable>: UIViewControllerRepresentable {
    let preparationHandler: () async throws -> ActivityType

    func makeUIViewController(context: Context) -> GroupActivitySharingController {
        GroupActivitySharingController(preparationHandler: preparationHandler)
    }

    func updateUIViewController(_: GroupActivitySharingController, context: Context) {}
}
```

### GameModel.swift
Path: `GuessTogether/Models/GameModel.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
A model that represents the current state of the game
  in the SharePlay group session.
*/

import Foundation
import GroupActivities

struct GameModel: Codable, Hashable, Sendable {
    /// The game's current state, which includes pre-game and in-game stages.
    var stage: ActivityStage = .categorySelection
    
    /// A set of categories that don't apply to the current game.
    var excludedCategories = Set<String>()
    
    /// A record of all the player's turns throughout the game, which the app updates when the player completes a turn.
    var turnHistory: [Participant.ID] = []
    
    /// The ending time of the current round, which the app sets at the beginning of each turn.
    var currentRoundEndTime: Date?
    
    /// The game's current secret phrase, which the app updates as it presents each new card.
    var currentPhrase: PhraseManager.Phrase?
    
    /// The phrases the game can't present again to the players, which the app updates as it presents each new card.
    var usedPhrases = Set<PhraseManager.Phrase>()
}

extension GameModel {
    /// The app's states during gameplay.
    enum GameStage: Codable, Hashable, Sendable {
        case beforePlayersTurn
        case duringPlayersTurn
        case afterPlayersTurn
    }
    
    enum ActivityStage: Codable, Hashable, Sendable {
        case categorySelection
        case teamSelection
        case inGame(GameStage)
        
        var isInGame: Bool {
            if case .inGame = self {
                true
            } else {
                false
            }
        }
    }
}
```

### SessionController.swift
Path: `GuessTogether/GroupActivity/SessionController.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The controller manages the app's active SharePlay session.
*/

import GroupActivities
import Observation

@Observable @MainActor
final class SessionController {
    let session: GroupSession<GuessTogetherActivity>
    let messenger: GroupSessionMessenger
    let systemCoordinator: SystemCoordinator
    
    var game: GameModel {
        get {
            gameSyncStore.game
        }
        set {
            if newValue != gameSyncStore.game {
                gameSyncStore.game = newValue
                shareLocalGameState(newValue)
            }
        }
    }
    
    var gameSyncStore = GameSyncStore() {
        didSet {
            gameStateChanged()
        }
    }

    var players = [Participant: PlayerModel]() {
        didSet {
            if oldValue != players {
                updateCurrentPlayer()
                updateLocalParticipantRole()
            }
        }
    }
    
    var localPlayer: PlayerModel {
        get {
            players[session.localParticipant]!
        }
        set {
            if newValue != players[session.localParticipant] {
                players[session.localParticipant] = newValue
                shareLocalPlayerState(newValue)
            }
        }
    }
    
    init?(_ groupSession: GroupSession<GuessTogetherActivity>, appModel: AppModel) async {
        guard let groupSystemCoordinator = await groupSession.systemCoordinator else {
            return nil
        }

        session = groupSession

        // Create the group session messenger for the session controller, which it uses to keep the game in sync for all participants.
        messenger = GroupSessionMessenger(session: session)

        systemCoordinator = groupSystemCoordinator

        // Create a representation of the local participant.
        localPlayer = PlayerModel(
            id: session.localParticipant.id,
            name: appModel.playerName
        )
        appModel.showPlayerNameAlert = localPlayer.name.isEmpty
        
        observeRemoteParticipantUpdates()
        configureSystemCoordinator()
        
        session.join()
    }
    
    func updateSpatialTemplatePreference() {
        switch game.stage {
            case .categorySelection:
                systemCoordinator.configuration.spatialTemplatePreference = .sideBySide
            case .teamSelection:
                systemCoordinator.configuration.spatialTemplatePreference = .custom(TeamSelectionTemplate())
            case .inGame:
                systemCoordinator.configuration.spatialTemplatePreference = .custom(GameTemplate())
        }
    }
    
    func updateLocalParticipantRole() {
        // Set and unset the participant's spatial template role based on updating game state.
        switch game.stage {
            case .categorySelection:
                systemCoordinator.resignRole()
            case .teamSelection:
                switch localPlayer.team {
                case .none:
                    systemCoordinator.resignRole()
                case .blue:
                    systemCoordinator.assignRole(TeamSelectionTemplate.Role.blueTeam)
                case .red:
                    systemCoordinator.assignRole(TeamSelectionTemplate.Role.redTeam)
                }
            case .inGame:
                if localPlayer.isPlaying {
                    systemCoordinator.assignRole(GameTemplate.Role.player)
                } else if let currentPlayer {
                    if currentPlayer.team == localPlayer.team {
                        systemCoordinator.assignRole(GameTemplate.Role.activeTeam)
                    } else {
                        systemCoordinator.resignRole()
                    }
                }
        }
    }
    
    func configureSystemCoordinator() {
        // Let the system coordinator show each players' spatial Persona in the immersive space.
        systemCoordinator.configuration.supportsGroupImmersiveSpace = true
        
        Task {
            // Wait for gameplay updates from participants.
            for await localParticipantState in systemCoordinator.localParticipantStates {
                localPlayer.seatPose = localParticipantState.seat?.pose
            }
        }
    }

    func enterTeamSelection() {
        game.stage = .teamSelection
        game.currentRoundEndTime = nil
        game.turnHistory.removeAll()
    }
    
    func joinTeam(_ team: PlayerModel.Team?) {
        localPlayer.team = team
    }
    
    func startGame() {
        game.stage = .inGame(.beforePlayersTurn)
    }
    
    func beginTurn() {
        nextCard(successful: false)
        
        // Set the new turn game state.
        game.stage = .inGame(.duringPlayersTurn)
        game.currentRoundEndTime = .now.addingTimeInterval(30)
        
        // Wait thirty seconds before ending the current turn.
        let sleepUntilTime = ContinuousClock.now.advanced(by: .seconds(30))
        Task {
            try await Task.sleep(until: sleepUntilTime)
            if case .inGame(.duringPlayersTurn) = game.stage {
                game.stage = .inGame(.afterPlayersTurn)
            }
        }
    }
    
    func nextCard(successful: Bool) {
        guard localPlayer.isPlaying else {
            return
        }
        
        if successful {
            localPlayer.score += 1
        }
        
        // Retrieve a random secret phrase from the phrase manager.
        let nextPhrase = PhraseManager.shared.randomPhrase(
            excludedCategories: game.excludedCategories,
            usedPhrases: game.usedPhrases
        )
        
        game.usedPhrases.insert(nextPhrase)
        game.currentPhrase = nextPhrase
    }
    
    func endTurn() {
        guard game.stage.isInGame, localPlayer.isPlaying else {
            return
        }
        
        game.turnHistory.append(session.localParticipant.id)
        game.currentRoundEndTime = nil
        game.stage = .inGame(.beforePlayersTurn)
        
        if playerAfterLocalParticipant != localPlayer {
            localPlayer.isPlaying = false
        }
    }
    
    func endGame() {
        game.stage = .categorySelection
    }
    
    func gameStateChanged() {
        if game.stage == .categorySelection {
            localPlayer.isPlaying = false
            localPlayer.score = 0
        }
        
        updateSpatialTemplatePreference()
        updateCurrentPlayer()
        updateLocalParticipantRole()
    }
}
```

### SessionController+PlayerOrder.swift
Path: `GuessTogether/GroupActivity/SessionController+PlayerOrder.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
A session controller extension that sorts the players in the app's current game.
*/

import Foundation
import GroupActivities

extension SessionController {
    func updateCurrentPlayer() {
        if game.stage.isInGame, localParticipantShouldBecomeActivePlayer {
            localPlayer.isPlaying = true
        }
    }
    
    var playerOrder: [Participant] {
        let firstPlayer = players.lazy.filter {
            $0.value.team != nil
        }
        .sorted(using: KeyPathComparator(\.key.id))
        .first?
        .value
        
        guard let firstPlayer else { return [] }
        guard let firstTeam = firstPlayer.team else { return [] }
        
        let secondTeam: PlayerModel.Team = switch firstTeam {
            case .blue: .red
            case .red: .blue
        }
        
        let sortedFirstTeam = players.filter {
            $0.value.team == firstTeam
        }
        .keys
        .sorted(using: KeyPathComparator(\.id))
        
        let sortedSecondTeam = players.filter {
            $0.value.team == secondTeam
        }
        .keys
        .sorted(using: KeyPathComparator(\.id))
        
        return sortedFirstTeam + sortedSecondTeam
    }
    
    var playerBeforeLocalParticipant: Participant? {
        guard let localParticipantIndex = playerOrder.firstIndex(of: session.localParticipant) else {
            return nil
        }
        
        if localParticipantIndex == 0 {
            return playerOrder.last
        } else {
            return playerOrder[localParticipantIndex - 1]
        }
    }
    
    var playerAfterLocalParticipant: PlayerModel? {
        guard let localParticipantIndex = playerOrder.firstIndex(of: session.localParticipant) else {
            return nil
        }
        
        let participant = if playerOrder.indices.contains(localParticipantIndex + 1) {
            playerOrder[localParticipantIndex + 1]
        } else {
            playerOrder.first
        }
        
        guard let participant else {
            return nil
        }
        
        return players[participant]
    }
    
    var currentPlayer: PlayerModel? {
        players.values.first(where: \.isPlaying)
    }
    
    var activeTeam: PlayerModel.Team? {
        return currentPlayer?.team
    }
    
    var localParticipantShouldBecomeActivePlayer: Bool {
        guard let playerBeforeLocalParticipant else {
            return false
        }
        
        guard let lastPlayer = game.turnHistory.last else {
            return playerOrder.first == session.localParticipant
        }
        
        let shouldBecomeActive = (lastPlayer == playerBeforeLocalParticipant.id)
        return shouldBecomeActive
    }
}
```

### SessionController+RemoteParticipantSynchronization.swift
Path: `GuessTogether/GroupActivity/SessionController+RemoteParticipantSynchronization.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
A session controller extension that synchronizes the app's state with the SharePlay group session.
*/

import GroupActivities

extension SessionController {
    func shareLocalPlayerState(_ newValue: PlayerModel) {
        Task {
            do {
                // Send local player state with the group session messenger.
                try await messenger.send(newValue)
            } catch {
                print("The app can't send the player state message due to: \(error)")
            }
        }
    }
    
    func shareLocalGameState(_ newValue: GameModel) {
        gameSyncStore.editCount += 1
        gameSyncStore.lastModifiedBy = session.localParticipant
    
        let message = GameMessage(
            game: newValue,
            editCount: gameSyncStore.editCount
        )
        Task {
            do {
                // Send local game state with the group session messenger.
                try await messenger.send(message)
            } catch {
                print("The app can't send the game state message due to: \(error)")
            }
        }
    }
    
    func observeRemoteParticipantUpdates() {
        observeActiveRemoteParticipants()
        observeRemoteGameModelUpdates()
        observeRemotePlayerModelUpdates()
    }
    
    private func observeRemoteGameModelUpdates() {
        Task {
            // Listen for game state messages from other players with the group session messenger.
            // Update local game state with the returned message and context.
            for await (message, context) in messenger.messages(of: GameMessage.self) {
                let senderID = context.source.id
                
                let editCount = gameSyncStore.editCount
                let gameLastModifiedBy = gameSyncStore.lastModifiedBy ?? session.localParticipant
                let shouldAcceptMessage = if message.editCount > editCount {
                    true
                } else if message.editCount == editCount && senderID > gameLastModifiedBy.id {
                    true
                } else {
                    false
                }
                
                guard shouldAcceptMessage else {
                    continue
                }
                
                if message.game != gameSyncStore.game {
                    gameSyncStore.game = message.game
                }
                gameSyncStore.editCount = message.editCount
                gameSyncStore.lastModifiedBy = context.source
            }
        }
    }
    
    private func observeRemotePlayerModelUpdates() {
        Task {
            for await (player, context) in messenger.messages(of: PlayerModel.self) {
                players[context.source] = player
            }
        }
    }
    
    private func observeActiveRemoteParticipants() {
        // Create a list of remote participants by removing the local participant from the group
        // session's list of active participants.
        let activeRemoteParticipants = session.$activeParticipants.map {
            $0.subtracting([self.session.localParticipant])
        }
        .withPrevious()
        .values
        
        Task {
            // Listen for game state messages from other players with the group session messenger.
            // Update local game state with the returned message and context.
            for await (oldActiveParticipants, currentActiveParticipants) in activeRemoteParticipants {
                let oldActiveParticipants = oldActiveParticipants ?? []
                
                let newParticipants = currentActiveParticipants.subtracting(oldActiveParticipants)
                let removedParticipants = oldActiveParticipants.subtracting(currentActiveParticipants)
                
                if !newParticipants.isEmpty {
                    // Send new participants the current state of the game.
                    do {
                        let gameMessage = GameMessage(
                            game: game,
                            editCount: gameSyncStore.editCount
                        )
                        try await messenger.send(gameMessage, to: .only(newParticipants))
                    } catch {
                        print("Failed to send game catchup message, \(error)")
                    }
                    
                    // Send new participants the player model of the local participant.
                    do {
                        try await messenger.send(localPlayer, to: .only(newParticipants))
                    } catch {
                        print("Failed to send player catchup message, \(error)")
                    }
                }

                // Remove any participants that have left from the active players dictionary.
                for participant in removedParticipants {
                    players[participant] = nil
                }
            }
        }
    }
    
    struct GameSyncStore {
        var editCount: Int = 0
        var lastModifiedBy: Participant?
        var game = GameModel()
    }
}

struct GameMessage: Codable, Sendable {
    let game: GameModel
    let editCount: Int
}
```

### GameTemplate.swift
Path: `GuessTogether/SpatialPersonaTemplates/GameTemplate.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The custom spatial template used to arrange spatial Personas
  during Guess Together's game stage.
*/

import GroupActivities
import Spatial

/// The team selection template contains three sets of seats:
///
/// 1. An seat to the left of the app window for the active player.
/// 2. Two seats to the right of the app window for the active player's
///    teammates.
/// 3. Five seats in front of the app window for the inactive team-members
///    and any audience members.
///
/// ```
///                  +--------------------+
///                  |   Guess Together   |
///                  |     app window     |
///                  +--------------------+
///
///
/// Active Player  %                       $  Active Team
///                                        $
///
///                      *  *  *  *  *
///
///                         Audience
///
/// ```
struct GameTemplate: SpatialTemplate {
    enum Role: String, SpatialTemplateRole {
        case player
        case activeTeam
    }
    
    static let playerPosition = Point3D(x: -2, z: 3)
    
    /// An array that represents the order the game adds participants to spatial template positions.
    var elements: [any SpatialTemplateElement] {
        let activeTeamCenterPosition = SpatialTemplateElementPosition.app.offsetBy(x: 2, z: 3)

        let playerSeat = SpatialTemplateSeatElement(
            position: .app.offsetBy(x: Self.playerPosition.x, z: Self.playerPosition.z),
            direction: .lookingAt(activeTeamCenterPosition),
            role: Role.player
        )
        
        let activeTeamSeats: [any SpatialTemplateElement] = [
            .seat(
                position: activeTeamCenterPosition.offsetBy(x: 0, z: -0.5),
                direction: .lookingAt(playerSeat),
                role: Role.activeTeam
            ),
            .seat(
                position: activeTeamCenterPosition.offsetBy(x: 0, z: 0.5),
                direction: .lookingAt(playerSeat),
                role: Role.activeTeam
            )
        ]
        
        let audienceSeats: [any SpatialTemplateElement] = [
            .seat(position: .app.offsetBy(x: 0, z: 5)),
            .seat(position: .app.offsetBy(x: 1, z: 5)),
            .seat(position: .app.offsetBy(x: -1, z: 5)),
            .seat(position: .app.offsetBy(x: 2, z: 5)),
            .seat(position: .app.offsetBy(x: -2, z: 5))
        ]
        
        return audienceSeats + [playerSeat] + activeTeamSeats
    }
}
```

### TeamSelectionTemplate.swift
Path: `GuessTogether/SpatialPersonaTemplates/TeamSelectionTemplate.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The custom spatial template used to arrange spatial Personas
  during Guess Together's team-selection stage.
*/

import GroupActivities

/// The team selection template contains three sets of seats:
///
/// 1. Five audience seats that participants are initially placed in.
/// 2. Three Blue Team seats that participants are moved to
///    when they join team Blue.
/// 3. Three Red Team seats.
///
/// ```
///                +--------------------+
///                |   Guess Together   |
///                |     app window     |
///                +--------------------+
///
///
///              %                       $
///                %                   $
///   Blue Team      %               $      Red Team
///                    *  *  *  *  *
///
///                       Audience
/// ```
struct TeamSelectionTemplate: SpatialTemplate {
    enum Role: String, SpatialTemplateRole {
        case blueTeam
        case redTeam
    }
    
    /// An array of seating positions the game uses to position spatial Personas during the team-selection stage.
    ///
    /// The game fills the seats with participants based on the order of the array's elements.
    let elements: [any SpatialTemplateElement] = [
        // Blue team:
        .seat(position: .app.offsetBy(x: -2.5, z: 3.5), role: Role.blueTeam),
        .seat(position: .app.offsetBy(x: -3.0, z: 3.0), role: Role.blueTeam),
        .seat(position: .app.offsetBy(x: -3.5, z: 2.5), role: Role.blueTeam),
        
        // Starting positions:
        .seat(position: .app.offsetBy(x: 0, z: 4)),
        .seat(position: .app.offsetBy(x: 1, z: 4)),
        .seat(position: .app.offsetBy(x: -1, z: 4)),
        .seat(position: .app.offsetBy(x: 2, z: 4)),
        .seat(position: .app.offsetBy(x: -2, z: 4)),
        
        // Red team:
        .seat(position: .app.offsetBy(x: 2.5, z: 3.5), role: Role.redTeam),
        .seat(position: .app.offsetBy(x: 3.0, z: 3.0), role: Role.redTeam),
        .seat(position: .app.offsetBy(x: 3.5, z: 2.5), role: Role.redTeam)
    ]
}
```

## Draw Together sample (GroupActivities)

Source root: `DrawingContentInAGroupSession/DrawTogether`

### DrawTogether.entitlements
Path: `DrawTogether/DrawTogether.entitlements`

```entitlements
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>com.apple.developer.group-session</key>
	<true/>
</dict>
</plist>
```

### DrawTogether.swift
Path: `DrawTogether/Model/DrawTogether.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The activity that users use to draw together.
*/

import Foundation
import GroupActivities

struct DrawTogether: GroupActivity {
    var metadata: GroupActivityMetadata {
        var metadata = GroupActivityMetadata()
        metadata.title = NSLocalizedString("Draw Together", comment: "Title of group activity")
        metadata.type = .generic
        return metadata
    }
}
```

### ContentView.swift
Path: `DrawTogether/View/ContentView.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The primary entry point for the app's user interface.
*/

import SwiftUI
import GroupActivities

struct ContentView: View {
    @StateObject var canvas = Canvas()

    var body: some View {
        VStack {
            HStack {
                Spacer()
                StrokeColorIndicator(color: canvas.strokeColor.uiColor)
            }
            .padding()

            ZStack {
                CanvasView(canvas: canvas)
                PhotoPlacementView(canvas: canvas)
            }

            ControlBar(canvas: canvas)
                .padding()

        }
        .task {
            for await session in DrawTogether.sessions() {
                canvas.configureGroupSession(session)
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
```

### ControlBar.swift
Path: `DrawTogether/View/ControlBar.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
A view that contains the buttons for interacting with the canvas or app.
*/

import SwiftUI
import GroupActivities
import PhotosUI

struct ControlBar: View {
    @ObservedObject var canvas: Canvas
    @StateObject var groupStateObserver = GroupStateObserver()
    @State private var selectedItem: PhotosPickerItem? = nil

    var body: some View {
        HStack {
            if canvas.groupSession == nil && groupStateObserver.isEligibleForGroupSession {
                Button {
                    canvas.startSharing()
                } label: {
                    Image(systemName: "person.2.fill")
                }
                .buttonStyle(.borderedProminent)
            }

            Spacer()

            if canvas.groupSession != nil {
                PhotosPicker(
                    selection: $selectedItem,
                    matching: .images,
                    photoLibrary: .shared()) {
                        Image(systemName: "photo.fill")
                            .foregroundColor(Color.white)
                            .background(Color.accentColor)
                }
                    .onChange(of: selectedItem) { _, newItem in
                        Task {
                            // Retrieve the selected asset in the form of Data
                            if let data = try? await newItem?.loadTransferable(type: Data.self) {
                                canvas.selectedImageData = data
                            }
                        }
                    }
            }

            Button {
                canvas.reset()
            } label: {
                Image(systemName: "trash.fill")
            }
        }
        .buttonStyle(.bordered)
        .controlSize(.large)
    }
}

struct ControlBar_Previews: PreviewProvider {
    static var previews: some View {
        ControlBar(canvas: Canvas())
            .previewLayout(.sizeThatFits)
    }
}
```

### Canvas.swift
Path: `DrawTogether/Model/Canvas.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
A model that represents the canvas to draw on.
*/

import Foundation
import Combine
import SwiftUI
import GroupActivities

struct CanvasImage: Identifiable {
    var id: UUID
    let location: CGPoint
    let imageData: Data
}

@MainActor
class Canvas: ObservableObject {
    @Published var strokes = [Stroke]()
    @Published var activeStroke: Stroke?
    @Published var images = [CanvasImage]()
    @Published var selectedImageData: Data?
    let strokeColor = Stroke.Color.random

    var subscriptions = Set<AnyCancellable>()
    var tasks = Set<Task<Void, Never>>()

    func addPointToActiveStroke(_ point: CGPoint) {
        let stroke: Stroke
        if let activeStroke = activeStroke {
            stroke = activeStroke
        } else {
            stroke = Stroke(color: strokeColor)
            activeStroke = stroke
        }

        stroke.points.append(point)

        if let messenger = messenger {
            Task {
                try? await messenger.send(UpsertStrokeMessage(id: stroke.id, color: stroke.color, point: point))
            }
        }
    }

    func finishStroke() {
        guard let activeStroke = activeStroke else {
            return
        }

        strokes.append(activeStroke)
        self.activeStroke = nil
    }

    func finishImagePlacement(location: CGPoint) {
        guard let selectedImageData = selectedImageData, let journal = journal else {
            return
        }

        Task(priority: .userInitiated) {
            try await journal.add(selectedImageData, metadata: ImageMetadataMessage(location: location))
        }

        self.selectedImageData = nil
    }

    func reset() {
        // Clear the local drawing canvas.
        strokes = []
        images = []

        // Tear down the existing groupSession.
        messenger = nil
        journal = nil
        tasks.forEach { $0.cancel() }
        tasks = []
        subscriptions = []
        if groupSession != nil {
            groupSession?.leave()
            groupSession = nil
            self.startSharing()
        }
    }

    var pointCount: Int {
        return strokes.reduce(0) { $0 + $1.points.count }
    }

    @Published var groupSession: GroupSession<DrawTogether>?
    var messenger: GroupSessionMessenger?
    var journal: GroupSessionJournal?

    func startSharing() {
        Task {
            do {
                _ = try await DrawTogether().activate()
            } catch {
                print("Failed to activate DrawTogether activity: \(error)")
            }
        }
    }

    func configureGroupSession(_ groupSession: GroupSession<DrawTogether>) {
        strokes = []

        self.groupSession = groupSession
        let messenger = GroupSessionMessenger(session: groupSession)
        self.messenger = messenger
        let journal = GroupSessionJournal(session: groupSession)
        self.journal = journal

        groupSession.$state
            .sink { state in
                if case .invalidated = state {
                    self.groupSession = nil
                    self.reset()
                }
            }
            .store(in: &subscriptions)

        groupSession.$activeParticipants
            .sink { activeParticipants in
                let newParticipants = activeParticipants.subtracting(groupSession.activeParticipants)

                Task {
                    try? await messenger.send(CanvasMessage(strokes: self.strokes, pointCount: self.pointCount), to: .only(newParticipants))
                }
            }
            .store(in: &subscriptions)

        var task = Task {
            for await (message, _) in messenger.messages(of: UpsertStrokeMessage.self) {
                handle(message)
            }
        }
        tasks.insert(task)

        task = Task {
            for await (message, _) in messenger.messages(of: CanvasMessage.self) {
                handle(message)
            }
        }
        tasks.insert(task)

        task = Task {
            for await images in journal.attachments {
                await handle(images)
            }
        }
        tasks.insert(task)

        groupSession.join()
    }

    func handle(_ message: UpsertStrokeMessage) {
        if let stroke = strokes.first(where: { $0.id == message.id }) {
            stroke.points.append(message.point)
        } else {
            let stroke = Stroke(id: message.id, color: message.color)
            stroke.points.append(message.point)
            strokes.append(stroke)
        }
    }

    func handle(_ message: CanvasMessage) {
        guard message.pointCount > self.pointCount else { return }
        self.strokes = message.strokes
    }

    func handle(_ attachments: GroupSessionJournal.Attachments.Element) async {
        // Ensure that the canvas always has all the images from this sequence.
        self.images = await withTaskGroup(of: CanvasImage?.self) { group in
            var images = [CanvasImage]()

            attachments.forEach { attachment in
                group.addTask {
                    do {
                        let metadata = try await attachment.loadMetadata(of: ImageMetadataMessage.self)
                        let imageData = try await attachment.load(Data.self)
                        return .init(id: attachment.id, location: metadata.location, imageData: imageData)
                    } catch { return nil }
                }
            }

            for await image in group {
                if let image {
                    images.append(image)
                }
            }

            return images
        }
    }
}
```

### Messages.swift
Path: `DrawTogether/Model/Messages.swift`

```swift
/*
See the LICENSE.txt file for this sample's licensing information.

Abstract:
The messages between multiple participants in a group session.
*/

import Foundation
import SwiftUI

struct UpsertStrokeMessage: Codable {
    let id: UUID
    let color: Stroke.Color
    let point: CGPoint
}

struct CanvasMessage: Codable {
    let strokes: [Stroke]
    let pointCount: Int
}

struct ImageMetadataMessage: Codable {
    let location: CGPoint
}
```
