/* Copyright (c) 2021-23 MIT 6.102/6.031 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */

import assert from 'assert';
import fs from 'fs';
import { Deferred } from './Deferred';

/**
 * Enum of possible card states in a Memory Scramble game.
 * Either the card is 'FacingUp', 'FacingDown', or 'Removed'
 */
enum CardState {
    FacingUp = "up",
    FacingDown = "down",
    Removed = "none"
}

/**
 * Immutable Coordinate in the Memory Scramble game, (row, column) of the gameboard
 */
export class Coordinate2D {

    private readonly _row: number;
    private readonly _column: number;

    // Abstraction Function
    // AF(_row, _column) = Coordinate of card in the '_row'th row and '_column'th column of the gameboard.
    //
    // Representation Invariant
    // - '_row' >= 0
    // - '_column' >= 0
    //
    // Safety from Rep Exposure
    // - all instance fields are private, readonly, and immutable
    // - no instance methods take in a mutable object as a parameter
    // - no instance methods return a mutable object as return value

    /**
     * Creates a Coordinate of given (row, column)
     * @param row row of coordinate in the Memory Scramble game
     * @param col column of coordinate in the Memory Scramble game
     */
    public constructor(row: number, column: number) {
        this._row = row;
        this._column = column;
        this.checkRep();
    }

    private checkRep(): void {
        assert(this._row >= 0);
        assert(this._column >= 0);
    }

    public get row(): number {
        return this._row;
    }

    public get column(): number {
        return this._column;
    }

    /**
     * Checks if two Coordinate2D objects are equal
     * 
     * @param that Coordinate2D object to compare
     * @returns true if this represents the same coordinate as that
     *          false otherwise.
     */
    public equalValue(that: Coordinate2D): boolean {
        return this._row === that._row && this._column === that._column;
    }
}

/**
 * Mutable Player of the Memory Scramble game.
 */
export class Player {
    private readonly _id: string;
    private readonly _control: Set<Coordinate2D>;
    private readonly _relinquished: Set<Coordinate2D>;
    private _blocked: boolean = false;

    // Abstraction Function
    //  AF(_id, _control, _relinquished, _blocked) = a Player of the Memory Scramble game with ID '_id'.
    //  It controls cards at coordinates ('coord'.row, 'coord'.column) for every Coordinate2D object 'coord'
    //  in '_control' and has recently relinquished control of cards at coordiantes ('coord'.row, 'coord'.column)
    //  for every Coordinate 2D object 'coord' in '_relinquished'. If '_blocked' is true, then the Player is
    //  currently waiting for a card to become available for them to control and cannot make any other moves on
    //  the gameboard. Otherwise, the Player is free to play the game according to Memory Scramble rules.

    // Representation Invariant
    //  - '_control'.size <= 2
    //  - '_relinquished'.size <= 2

    // Safety from Rep Exposure
    //  - All mutable instance variables are private and readonly.
    //  - No instance methods return a reference to the mutable instance fields.
    //  - No instance methods take in a reference to a mutable object.

    /**
     * Creates a Player of given id. Initially has no coordinates it controls / relinquished.
     * Initially not blocked from making a new move in the game.
     * 
     * @param playerId ID of player
     */
    public constructor (playerId: string) {
        this._id = playerId;
        this._control = new Set([]);
        this._relinquished = new Set([]);
        this.checkRep();
    }

    private checkRep(): void{

        // _control.size <= 2
        assert(this._control.size <= 2);

        // _relinquished.size <= 2
        assert(this._relinquished.size <= 2);
    }

    public get id(): string {
        return this._id;
    }

    public get blocked(): boolean {
        return this._blocked;
    }

    public set blocked(isBlocked: boolean) {
        this._blocked = isBlocked;
    }

    /**
     * Adds coordinates (row, column) to the list of coordinates of cards this player controls.
     * @param row of card to control.
     * @param column of card to control
     * @throws if adding a coordinate to player's control makes the player be in control of > 2 coordinates
     */
    public addToControl(row: number, column: number): void {
        this._control.add(new Coordinate2D(row, column));
        this.checkRep();
    }

    /**
     * Removes all coordinates (row, column) of cards from this player's control.
     */
    public clearControl(): void {
        this._control.clear();
        this.checkRep();
    }

    /**
     * @returns all coordiantes (row, column) of cards in this player's control.
     */
    public getControl(): Array<Coordinate2D> {
        const control: Array<Coordinate2D> = [];
        for (const coord of this._control) {
            control.push(coord);
        }
        return control;
    }

    /**
     * Relinquishes the player's control from coordinates (row, column)
     * 
     * @param row of card to relinquish
     * @param column of card to relinquish
     * @throws if adding coordinate to player's relinquished coordinates makes it so that
     *         the player has > 2 recently relinquished coordinates
     */
    public addToRelinquished(row: number, column: number): void {
        this._relinquished.add(new Coordinate2D(row, column));
        this.checkRep();
    }

    /**
     * Untracks all currently relinquished cards of this player.
     */
    public clearRelinquished(): void {
        this._relinquished.clear();
        this.checkRep();
    }

    /**
     * @returns all relinquished coordinates (row, column) of cards that this player
     * is keeping track of.
     */
    public getRelinquished(): Array<Coordinate2D> {
        const relinquished: Array<Coordinate2D> = [];
        for (const coord of this._relinquished) {
            relinquished.push(coord);
        }
        return relinquished;
    }
}

/**
 * Gameboard of Memory Scramble game
 * Mutable and concurrency safe
 */
export class Board {
    
    private readonly rows: number;
    private readonly columns: number;

    private cardTexts: Array<Array<string>> = [];
    private readonly cardStates: Array<Array<CardState>> = [];

    private readonly players: Map<string, Player> = new Map([]);

    private readonly owners: Array<Array<string | undefined>> = [];
    private readonly waiting: Array<Array<Set<string>>> = [];
    private readonly blocks: Array<Array<Map<string, Deferred<void>>>> = [];

    private readonly watches: Map<string, Deferred<void>> = new Map([]);

    // Abstraction Function
    // AF(rows, columns, cardTexts, cardStates, players, owners, waiting, blocks , watches) = 
    //  A Memory Scramble gameboard that consists of 'rows' rows and 'columns' columns cards. The game is being played
    //  by plaers in 'players'.values(), and the game has cards with text 'cardTexts'[i][j] and state 'cardStates'[i][j]
    //  (FacingDown, FacingUp, or Removed) at the ith row and jth column of the gameboard. Each card at the ith row and
    //  jth column of the board is owned by player with id 'owners'[i][j], or does not have an owner if 'owners'[i][j] is
    //  undefined. Players with id in 'waiting'[i][j] are waiting to get control of card at the ith row and jth column,
    //  and their promises are located in 'blocks'[i][j].get(id). Players with id in 'watches'.values() is watching the board.

    // Representation Invariant
    //  - 'rows', 'columns' > 0
    //  - 'cardTexts'.length, 'cardStates'.length, 'owners'.length, 'waiting'.length, 'blocks'.length === this.'rows'
    //  - 'cardTexts'[i].length, 'cardStates'[i].length, 'owners'[i].length, 'waiting'[i].length, 'blocks'[i].length
    //    === this.'columns' for all 0 <= i < this.'rows'
    //  - all unique string values in 'owners', 'waiting', 'blocks', 'watches' are in 'players'.keys()
    //  - for 0 <= i < this.'rows' and 0 <= j < this.'columns', there should not be an (i,j) where 'owners'[i][j] !== undefined
    //    and 'cardState'[i][j] === "down";
    //  - all string values in 'cardTexts' are non-empty and do not contain whitespace / newline.
    //  - for 0 <= i < this.'rows' and 0 <= j < this.'columns', 'waiting'[i][j].size === 'blocks'[i][j].size < 'players'.size
    //  - 'watches'.size <= 'players'.size

    // Safety from Rep Exposure
    //  - all instance fields and private and readonly
    //  - no instance methods return a reference to the mutable instance fields
    //  - mutable object taken as a parameter in constructor is defensively copied before being assigned to the instance field,
    //    so client holding reference to / mutating the cards parameter does not mutate this.cardTexts
    //  - other than the constructor, no other instance method takes in a reference to a mutable object as its parameter

    /**
     * Creates a new Board of size rows x columns containing cards that are in the cards array, in row major order.
     * Initial Board has no players and no players that are watching.
     * Every card has no owner nor players that are waiting, and is initially facing down.
     * 
     * @param rows height of gameboard, required > 0
     * @param columns width of gameboard, required > 0
     * @param cards array of cards in the gameboard, in row-major order
     */
    public constructor (rows: number, columns: number, cards: Array<Array<string>>) {

        this.rows = rows;
        this.columns = columns;

        // defensive copying for input of cards
        const newCards: Array<Array<string>> = [];
        for (let i = 0; i < this.rows; i++) {
            const cardRow = cards[i];
            assert(cardRow !== undefined);
            const newCardsRow = [];
            for (let j = 0; j < this.columns; j++) {
                const cardText = cardRow[j];
                assert(cardText !== undefined);
                newCardsRow.push(cardText);
            }
            newCards.push(newCardsRow);
        }

        this.cardTexts = newCards;

        for (let i = 0; i < this.rows; i++) {

            const cardStateRow: Array<CardState> = [];
            const ownerRow: Array<string | undefined> = [];
            const waitingRow: Array<Set<string>> =[];
            const blocksRow: Array<Map<string, Deferred<void>>> = [];

            for (let j = 0; j < this.columns; j++) {

                cardStateRow.push(CardState.FacingDown);
                ownerRow.push(undefined);
                waitingRow.push(new Set([]));
                blocksRow.push(new Map([]));
            }

            this.cardStates.push(cardStateRow);
            this.owners.push(ownerRow);
            this.waiting.push(waitingRow);
            this.blocks.push(blocksRow);
        }

        this.checkRep();
    }

    private checkRep(): void {
        // 'rows', 'columns' > 0
        assert(this.rows > 0);
        assert(this.columns > 0);

        // 'cardTexts'.length, 'cardStates'.length, 'owners'.length, 'waiting'.length, 'blocks'.length === this.'rows'
        assert(this.cardTexts.length === this.rows);
        assert(this.cardStates.length === this.rows);
        assert(this.owners.length === this.rows);
        assert(this.waiting.length === this.rows);
        assert(this.blocks.length === this.rows);

        const playersInOwners: Set<string> = new Set([]);
        const playersInWaiting: Set<string> = new Set([]);
        const playersInBlocks: Set<string> = new Set([]);

        for (let i = 0; i < this.rows; i++) {

            const cardTextRow = this.cardTexts[i];
            const cardStateRow = this.cardStates[i];
            const ownerRow = this.owners[i];
            const waitingRow = this.waiting[i];
            const blocksRow = this.blocks[i];

            assert(cardTextRow !== undefined && cardStateRow !== undefined);
            assert(ownerRow !== undefined && waitingRow !== undefined && blocksRow !== undefined);

            // 'cardTexts'[i].length, 'cardStates'[i].length, 'owners'[i].length, 'waiting'[i].length, 'blocks'[i].length
            // === this.'columns' for all 0 <= i < this.'rows'
            assert(cardTextRow.length === this.columns);
            assert(cardStateRow.length === this.columns);
            assert(ownerRow.length === this.columns);
            assert(waitingRow.length === this.columns);
            assert(blocksRow.length === this.columns);

            for (let j = 0; j < this.columns; j++) {

                // all string values in 'cardTexts' are non-empty and do not contain whitespace / newline.
                const thisCardText = cardTextRow[j];
                assert(thisCardText !== undefined);
                assert(thisCardText.match(/[^\s\n\r]+/));

                const thisCardState = cardStateRow[j];
                assert(thisCardState !== undefined);

                const thisOwner = ownerRow[j];
                if (thisOwner !== undefined) {
                    playersInOwners.add(thisOwner);
                }

                // for 0 <= i < this.'rows' and 0 <= j < this.'columns', there should not be an (i,j) where 'owners'[i][j] !== undefined
                // and 'cardState'[i][j] === CardState.FacingDown;
                if (thisCardState === "down") {
                    assert(thisOwner === undefined);
                }

                const waitingSet = waitingRow[j];
                assert(waitingSet !== undefined);
                for (const waiting of waitingSet) {
                    playersInWaiting.add(waiting);
                }

                const blocksMap = blocksRow[j];
                assert(blocksMap !== undefined);
                for (const blocks of blocksMap.keys()) {
                    playersInBlocks.add(blocks);
                }

                // for 0 <= i < this.'rows' and 0 <= j < this.'columns', 'waiting'[i][j].size === 'blocks'[i][j].size < 'players'.size
                assert(waitingSet.size === blocksMap.size);
                assert(waitingSet.size <= this.players.size);
            }
        }

        // all unique string values in 'owners', 'waiting', 'blocks', 'watches' are in 'players'.keys()
        for (const playerId of playersInOwners) {
            assert(this.players.has(playerId));
        }
        for (const playerId of playersInWaiting) {
            assert(this.players.has(playerId));
        }
        for (const playerId of playersInBlocks) {
            assert(this.players.has(playerId));
        }
        for(const playerId of this.watches.keys()) {
            assert(this.players.has(playerId));
        }

        // 'watches'.size <= 'players'.size
        assert(this.watches.size <= this.players.size);
    }

    /**
     * Make a new board by parsing a file
     * 
     * PS4 instruction: the specification of this method may not be changed.
     * 
     * @param filename path to game board file
     * @returns (a promise for) a new board with the size and cards from the file
     * @throws Error if the file cannot be read or is not a valid gameboard
     */
    public static async parseFromFile(filename: string): Promise<Board> {

        const result: string = await fs.promises.readFile(filename, {encoding: 'utf-8'});
        const lines: Array<string> = result.split(/\r?\n/);

        // parse the first line of the file, which contains dimensions of the gameboard
        assert(lines[0] !== undefined);
        assert(lines[0].match(/[0-9]+x[0-9]+/));
        const dimensions: Array<string> = lines[0].split("x");
        assert(dimensions[0] !== undefined && dimensions[1] !== undefined);
        const rows = parseInt(dimensions[0]);
        const columns = parseInt(dimensions[1]);

        // parse the rest of the file, which contains cards in row-major order
        const cards: Array<Array<string>> = [];
        for (let i = 0; i < rows; i++) {
            const row: Array<string> = [];
            for (let j = 0; j < columns; j++) {
                const text = lines[i*columns+j+1];
                assert(text !== undefined);
                assert(text.match(/[^\s\n\r]+/));
                row.push(text);
            }
            cards.push(row);
        }

        return new Board(rows, columns, cards);
    }

    /**
     * Converts this gameboard into a boardstate that can be parsed by the web server
     * from the perspective of player with playerId
     * 
     * @param playerId from whose perspective the board state is seen from
     * @returns board state of the gameboard, from the perspective of player with playerId
     */
    public boardState(playerId: string): string {

        let boardState = "";

        const dimensions = `${this.rows}x${this.columns}\n`;
        boardState += dimensions;

        // none: no card at that location (Removed)
        // down: card is FacingDown
        // up: card is FacingUp, controlled by another player, or by no one
        // my: card is FacingUp, controlled by player with playerId

        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.columns; j++) {
                let cardString = "";
                const cardState = this.getCard(i, j).state;
                const cardText = this.getCard(i, j).text;
                const currentOwner = this.getOwner(i, j);
                const isOwner = currentOwner !== undefined && currentOwner === playerId;

                if (cardState === "none") {
                    cardString += "none\n";
                }
                else if (cardState === "down") {
                    cardString += "down\n";
                }
                else if (cardState ==="up" && !isOwner) {
                    cardString += `up ${cardText}\n`;
                }
                else if (cardState === "up" && isOwner) {
                    cardString += `my ${cardText}\n`;
                }
                boardState += cardString;
            }
        }
        return boardState;
    }

    /**
     * Converts this gameboard into a string, following the boardstate format
     * above. However, this produces a boardstate from the general perspective
     * and does not reflect any player's ownership over any cards.
     * 
     * @returns board state of the gameboard
     */
    public toString(): string {

        let boardState = "";

        const dimensions = `${this.rows}x${this.columns}\n`;
        boardState += dimensions;

        // none: no card at that location (Removed)
        // down: card is FacingDown
        // up: card is FacingUp, controlled by another player, or by no one
        // my: card is FacingUp, controlled by player with playerId

        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.columns; j++) {
                let cardString = "";
                const cardState = this.getCard(i, j).state;
                const cardText = this.getCard(i, j).text;

                if (cardState === "none") {
                    cardString += "none\n";
                }
                else if (cardState === "down") {
                    cardString += "down\n";
                }
                else if (cardState === "up") {
                    cardString += `up ${cardText}\n`;
                }
                boardState += cardString;
            }
        }
        return boardState;
    }

    ////////////////////////
    //    GAME HELPERS    //
    ////////////////////////

    /**
     * Adds a player to the Memory Scramble game.
     * All players must be added to the game before participating
     * If player with playerId already exists in the game, new request is ignored.
     * 
     * @param playerId of player to add to the game
     */
    public setPlayer(playerId: string): void {

        if (this.players.has(playerId)) {
            return;
        }

        const player = new Player(playerId);
        this.players.set(playerId, player);
    }

    /**
     * Returns id of the player that owns the card at position (row, column)
     * 
     * @param row row of card, required 0 <= row < this.height
     * @param column column of card, required 0 <= column < this.width
     * @returns id of the player that owns the card at position (row, column)
     *          undefined if there is no owner of that position
     */
    private getOwner(row: number, column: number): string | undefined {
        const ownerRow = this.owners[row];
        assert(ownerRow !== undefined);
        return ownerRow[column];
    }

    /**
     * Sets player (or no player) to own a card at position (row, column)
     * Updates gameboard to reflect this change.
     * 
     * @param row row of card, required 0 <= row < this.height
     * @param column column of card, required 0 <= column < this.width
     * @param owner id of new owner of the card at (row, column)
     *              or undefined if there is no new owner of the card.
     */
    private setOwner(row: number, column: number, owner: string | undefined): void {

        const ownerRow = this.owners[row];
        assert(ownerRow !== undefined);
        ownerRow[column] = owner;
    }

    /**
     * Returns the text and state of the card at position (row, column)
     * 
     * @param row row of card, required 0 <= row < this.height
     * @param column column of card, required 0 <= column < this.width
     * @returns text and state of the card (FacingUp, FacingDown, or Removed) at (row, column)
     */
    private getCard(row: number, column: number): {text: string, state: CardState} {

        const cardTextRow = this.cardTexts[row];
        assert(cardTextRow !== undefined);
        const text = cardTextRow[column];
        assert(text !== undefined);

        const cardStateRow = this.cardStates[row];
        assert(cardStateRow !== undefined);
        const state = cardStateRow[column];
        assert(state !== undefined);

        return {text: text, state: state};
    }

    /**
     * Sets the state of the card at (row, column) to be newState
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, requipred 0 <= column < this.width
     * @param newState of the card, FacingUp, FacingDown, or Removed
     */
    private setCardState(row: number, column: number, newState: CardState): void {
        const cardStateRow = this.cardStates[row];
        assert(cardStateRow !== undefined);
        cardStateRow[column] = newState;
    }

    /**
     * @param waitingSet set of player ids waiting to get control at a certain coordinate
     * @returns a random player id from waitingSet
     */
    private getRandomId(waitingSet: Set<string>): string {
        const index: number = Math.floor(Math.random() * waitingSet.size);
        const id = [...waitingSet.values()][index];
        assert(id !== undefined);
        return id;
    }

    /**
     * If any player is waiting to control the card at (row, column),
     * picks one of the players waiting and gives them the control.
     * 
     * @param row row to assign a new owner at
     * @param column column to assign a new owner at
     */
    private undoBlock(row: number, column: number): void {

        const waitingRow = this.waiting[row];
        assert(waitingRow !== undefined);
        const waitingSet = waitingRow[column];
        assert(waitingSet !== undefined);

        if (waitingSet.size > 0) {

            const blocksRow = this.blocks[row];
            assert(blocksRow !== undefined);
            const blocksMap = blocksRow[column];
            assert(blocksMap !== undefined);

            const idToResolve = this.getRandomId(waitingSet);
            const toResolve = blocksMap.get(idToResolve);
            assert(toResolve !== undefined);
            toResolve.resolve();

            // waitingSet.delete(idToResolve);
            // blocksMap.delete(idToResolve);
        }
    }

    /**
     * Unblocks all players waiting to control the card at (row, column)
     * 
     * @param row row to unblock players at
     * @param column column to unblock players at
     */
    private undoAllBlocks(row: number, column: number): void {

        const waitingRow = this.waiting[row];
        assert(waitingRow !== undefined);
        const waitingSet = waitingRow[column];
        assert(waitingSet !== undefined);

        for (const player of waitingSet) {
            const blocksRow = this.blocks[row];
            assert(blocksRow !== undefined);
            const blocksMap = blocksRow[column];
            assert(blocksMap !== undefined);

            const toResolve = blocksMap.get(player);
            assert(toResolve !== undefined);
            toResolve.resolve();

            // waitingSet.delete(player);
            // blocksMap.delete(player);
        }
    }

    //////////////////
    //     FLIP     //
    //////////////////

    /**
     * Processes player flip command at position (row, column)
     * Updates gameboard and that player's Player object as necessary.
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, required 0 <= column < this.width
     * @param playerId of the player that made the flip command
     * @throws if id of the player has not been added to the game yet
     */
    public async turnCard(row: number, column: number, playerId: string): Promise<void> {

        // get player object
        const player = this.players.get(playerId);
        assert(player !== undefined);
        const numControl = player.getControl().length;
        const numRelinquished = player.getRelinquished().length;

        if (player.blocked) { return; }

        // CASE: player is attempting to flip their first card
        //       need to check if the player needs to be blocked
        //       if so, their request is blocked via await until they can try to flip this card again.
        //       if not, their request is handled normally.
        if (numControl === 0 && numRelinquished === 0){

            // request fails if there is no card at that location
            if (this.getCard(row, column).state === "none") { throw new Error("attempted to flip a removed card"); }

            // if card at that position does not have an owner, or if this player already controls that card,
            // then the player does not need to be blocked.
            if (this.getOwner(row, column) === undefined || this.getOwner(row, column) === playerId) {
                this.turnCardFirst(row, column, player);
                return;
            }

            // in other cases, this request needs to be blocked
            player.blocked = true;

            const blockDeferred = new Deferred<void>();

            const blocksRow = this.blocks[row];
            assert(blocksRow !== undefined);
            const blocksMap = blocksRow[column];
            assert(blocksMap !== undefined);
            blocksMap.set(playerId, blockDeferred);

            const waitingRow = this.waiting[row];
            assert(waitingRow !== undefined);
            const waitingSet = waitingRow[column];
            assert(waitingSet !== undefined);
            waitingSet.add(playerId);

            await blockDeferred.promise.then(async () => {
                waitingSet.delete(playerId);
                blocksMap.delete(playerId);
                player.blocked = false;
                this.turnCardFirst(row, column, player);
            });
        }
        // CASE: player is attempting to turn their second card
        else if (numControl === 1 && numRelinquished === 0) {
            this.turnCardSecond(row, column, player);
            return;
        }
        // CASE: player is attempting to turn their third card, where the previous two matched
        else if (numControl === 2) {
            this.turnCardThirdMatch(row, column, player);
            await this.turnCard(row, column, player.id);
        }
        // CASE: player is attempting to turn their third card, where the previous two did not match
        else if (numRelinquished > 0) {
            this.turnCardThirdNoMatch(row, column, player);
            await this.turnCard(row, column, player.id);
        }

        this.checkRep();
        return;
    }

    /**
     * Processes player attempting to turn over a card at position (row, column) for the first time.
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, required 0 <= column < this.width
     * @param player seeking to turn over card at position (row, column)
     */
    private turnCardFirst(row: number, column: number, player: Player): void {

        assert(!player.blocked);

        const cardState = this.getCard(row, column).state;

        // If there is no card there, the operation fails
        if (cardState === "none") { throw new Error("attempted to flip a removed card"); } // TODO throw errors when operations fail

        // If card is not controlled by another player, player takes control
        // If card is FacingDown, flip it so that it is FacingUp
        else if (this.getOwner(row, column) === undefined) {
            this.setOwner(row, column, player.id);
            player.addToControl(row, column);

            if (cardState === "down") {
                this.setCardState(row, column, CardState.FacingUp);
                this.resolveWatch();
            }
        }
    }

    /**
     * Processes player attempting to turn over a card at position (row, column) for the first time.
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, required 0 <= column < this.width
     * @param player seeking to turn over card at position (row, column)
     */
    private turnCardSecond(row: number, column: number, player: Player): void {

        const cardState = this.getCard(row, column).state;
        const currentOwner = this.getOwner(row, column);
        const control = player.getControl()[0]; // coordinates of card currently in player's control
        assert(control !== undefined);

        // If there is no card there, the operation fails.
        // The player also relinquishes control of their first card, but it remains face up for now
        // In addition, if the card is face up and controlled by a player (another player or themselves),
        // the operation fails. To avoid deadlocks, the operation does not block. The player also
        // relinquishes control of their first card, but it remains face up for now
        if (cardState === "none" || (cardState === "up" && currentOwner !== undefined)) {
            this.setOwner(control.row, control.column, undefined);
            player.clearControl();
            player.addToRelinquished(control.row, control.column);
            this.undoBlock(control.row, control.column);
            throw new Error("attempted to flip a removed or already controlled card");
        }

        // If the card is facing down, or if the card is face up but not controlled by a player,
        // - If it is face down, flip it so that it is facing up
        // - If the previous card and this card matches, the player stays in control of both cards.
        // - If the previous card and this card does not match, the player relinquishes both cards.
        else if (cardState === "down" || (cardState === "up" && currentOwner === undefined)) {

            if (cardState === "down") {
                this.setCardState(row, column, CardState.FacingUp);
                this.resolveWatch();
            }

            // check if the two cards match
            
            const text1 = this.getCard(control.row, control.column).text;
            const text2 = this.getCard(row, column).text;

            if (text1 === text2) {
                this.setOwner(row, column, player.id);
                player.addToControl(row, column);
            }
            else {
                this.setOwner(control.row, control.column, undefined);
                this.setOwner(row, column, undefined);
                player.clearControl();
                player.addToRelinquished(control.row, control.column);
                player.addToRelinquished(row, column);
                this.undoBlock(control.row, control.column);
                this.undoBlock(row, column);
            }
        }
    }

    /**
     * Processes player attempting to turn over a card at position (row, column) for the third time,
     * given that their previous two cards have matched.
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, required 0 <= column < this.width
     * @param player seeking to turn over card at position (row, column)
     */
    private turnCardThirdMatch(row: number, column: number, player: Player): void {

        // player currently has two cards in their control (matching pair)
        // these cards are removed from the board, and the player relinquishes control of them.
        const control: Array<Coordinate2D> = player.getControl();
        
        for (const coord of control) {
            this.setOwner(coord.row, coord.column, undefined);
            this.setCardState(coord.row, coord.column, CardState.Removed);
            this.resolveWatch();
            // any player waiting for the newly relinquished cards should be unblocked
            this.undoAllBlocks(coord.row, coord.column);
        }

        player.clearControl();
        player.clearRelinquished();

        // this.turnCard(row, column, player.id);
    }

    /**
     * Processes player attempting to turn over a card at position (row, column) for the third time,
     * given that their previous two cards have not matched.
     * 
     * @param row of card, required 0 <= row < this.height
     * @param column of card, required 0 <= column < this.width
     * @param player seeking to turn over card at position (row, column)
     */
    private turnCardThirdNoMatch(row: number, column: number, player: Player): void {

        // player currently has two cards they have relinquished (unmatching pair)
        // If those cards are still on the board, currently facing up, and not controlled by another
        // player, then they are turned face down.

        const relinquished: Array<Coordinate2D> = player.getRelinquished();
        
        for (const coord of relinquished) {
            const cardState = this.getCard(coord.row, coord.column).state;
            const owner = this.getOwner(coord.row, coord.column);
            
            if (cardState === "up" && owner === undefined) {
                this.setCardState(coord.row, coord.column, CardState.FacingDown);
                this.resolveWatch();
            }
        }

        player.clearControl();
        player.clearRelinquished();

        // this.turnCard(row, column, player.id);
    }

    /////////////////
    //     MAP     //
    /////////////////

    /**
     * Given an asynchronous function that converts a card's text to new text, promises to set this
     * gameboard's cards' texts to new texts that have been converted by the async function. While
     * it converts each card atomically and the conversion of all cards happen asynchronously,
     * changed card texts are only visible to all players after all cards texts have been updated.
     * 
     * @param f maps an existing card's text to new text. Must not be one-to-many
     * @param playerId player that is issuing the map command
     * @returns the board state, as described by this.toString(playerId) after the map call has completed.
     */
    public async map(f: (card: string) => Promise<string>, playerId: string): Promise<string> {

        // idea: have a promise for the entire Array<Array<string>>, with a promise for each row of
        //       Array<string>, then with a promise for each of the strings in each row.
        const arrayPromise: Array<Promise<Array<string>>> = [];

        for (let i = 0; i < this.rows; i++) {

            const textRow = this.cardTexts[i];
            assert(textRow !== undefined);

            const rowPromise: Array<Promise<string>> = [];
            for (let j = 0; j < this.columns; j++) {

                const text = textRow[j];
                assert(text !== undefined);

                const textPromise: Promise<string> = f(text);
                rowPromise.push(textPromise);
            }

            const row: Promise<Array<string>> = Promise.all(rowPromise);
            arrayPromise.push(row);
        }

        const newTextPromise: Promise<Array<Array<string>>> = Promise.all(arrayPromise);
        await newTextPromise.then((newText: Array<Array<string>>) => {
            this.cardTexts = newText;
            this.resolveWatch();
        });

        this.checkRep();
        return this.boardState(playerId);
    }

    ///////////////////
    //     WATCH     //
    ///////////////////

    /**
     * Processes a watch command for a player, blocking until any cards turn face up or face down,
     * are removed from the board, or their texts are changed. Players that are watch are not
     * blocked from making any other moves on the board.
     * 
     * @param playerId of player that is watching
     */
    public async watch(playerId: string): Promise<string> {
        const watchDeferred = new Deferred<void>();
        this.watches.set(playerId, watchDeferred);
        await watchDeferred.promise;
        this.watches.delete(playerId);
        this.checkRep();
        return this.boardState(playerId);
    }

    /**
     * Processes resolving a watch promise whenever there is a visible change on the gameboard.
     */
    private resolveWatch(): void {
        for (const watchDeferred of this.watches.values()) {
            watchDeferred.resolve();
        }
    }
}