import solders
from solders.pubkey import Pubkey
from solders import system_program
from solana.transaction import *
from spl.token import constants as spl_constants
from spl.token import instructions as assoc_instructions
from .instruction import *
from .state import *
from .state import Constants as ingl_constants
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from rich import print


async def ingl_init(
    payer_keypair: KeypairInput,
    upgrade_authority: KeypairInput,
    validator_pubkey: PubkeyInput,
    init_commission: int,
    max_primary_stake: int,
    nft_holders_share: int,
    initial_redemption_fee: int,
    is_validator_id_switchable: bool,
    unit_backing: int,
    redemption_fee_duration: int,
    proposal_quorum: int,
    creator_royalties: int,
    governance_expiration_time: int,
    rarities: List[int],
    rarity_names: List[str],
    twitter_handle: str,
    discord_invite: str,
    validator_name: str,
    collection_uri: str,
    website: str,
    default_uri: str,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    mint_pubkey, _mint_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_NFT_COLLECTION_KEY, "UTF-8")], get_program_id()
    )
    mint_authority_pubkey, _mint_authority_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_MINT_AUTHORITY_KEY, "UTF-8")], get_program_id()
    )
    (
        collection_holder_pubkey,
        _collection_holder_pubkey_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.COLLECTION_HOLDER_KEY, "UTF-8")], get_program_id()
    )
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(
        collection_holder_pubkey, mint_pubkey
    )
    metaplex_program_id = Pubkey.from_string(
        "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    )
    metadata_pda, _metadata_pda_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey)],
        metaplex_program_id,
    )
    master_edition_pda, _master_edition_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey), b"edition"],
        metaplex_program_id,
    )
    ingl_config_pubkey, _ingl_config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    uris_account_pubkey, _uris_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.URIS_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    this_program_data_pubkey, _this_program_data_bump = Pubkey.find_program_address(
        [bytes(get_program_id())], ingl_constants.BPF_LOADER_UPGRADEABLE
    )

    # registry_program_config_key, _registry_program_config_bump = Pubkey.find_program_address([b'config'], ingl_constants.REGISTRY_PROGRAM_ID)
    storage_key, _storage_bump = Pubkey.find_program_address(
        [b"storage"], ingl_constants.REGISTRY_PROGRAM
    )
    name_storage_meta = AccountMeta(
        Pubkey.find_program_address(
            [
                b"name_storage",
            ],
            ingl_constants.REGISTRY_PROGRAM,
        )[0],
        False,
        True,
    )
    upgrade_authority_meta = AccountMeta(upgrade_authority.pubkey, True, False)

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    collection_holder_meta = AccountMeta(collection_holder_pubkey, False, True)
    mint_account_meta = AccountMeta(mint_pubkey, False, True)
    mint_authority_meta = AccountMeta(mint_authority_pubkey, False, False)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    sysvar_rent_account_meta = AccountMeta(solders.sysvar.RENT, False, False)
    system_program_meta = AccountMeta(system_program.ID, False, False)
    this_program_data_meta = AccountMeta(this_program_data_pubkey, False, False)
    token_metadata_meta = AccountMeta(metadata_pda, False, True)
    metadata_program_id = AccountMeta(metaplex_program_id, False, False)
    associated_program_meta = AccountMeta(
        spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False
    )
    edition_meta = AccountMeta(master_edition_pda, False, True)
    ingl_config_meta = AccountMeta(ingl_config_pubkey, False, True)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    uris_account_meta = AccountMeta(uris_account_pubkey, False, True)
    validator_account_meta = AccountMeta(validator_pubkey.pubkey, False, True)
    # registry_program_config_meta = AccountMeta(registry_program_config_key, False, True)
    program_meta = AccountMeta(get_program_id(), False, False)
    team_account_meta = AccountMeta(ingl_constants.TEAM_ADDRESS, False, True)
    storage_account_meta = AccountMeta(storage_key, False, True)
    registry_program_meta = AccountMeta(ingl_constants.REGISTRY_PROGRAM, False, False)

    accounts = [
        payer_account_meta,
        ingl_config_meta,
        general_account_meta,
        uris_account_meta,
        sysvar_rent_account_meta,
        validator_account_meta,
        collection_holder_meta,
        mint_account_meta,
        mint_authority_meta,
        mint_associated_meta,
        token_metadata_meta,
        edition_meta,
        spl_program_meta,
        system_program_meta,
        this_program_data_meta,
        upgrade_authority_meta,
        program_meta,
        team_account_meta,
        storage_account_meta,
        name_storage_meta,
        # registry_program_config_meta,
        system_program_meta,
        # programs below
        associated_program_meta,
        spl_program_meta,
        metadata_program_id,
        registry_program_meta,
    ]
    # print(accounts)
    data = build_instruction(
        InstructionEnum.enum.Init(
            init_commission=init_commission,
            max_primary_stake=max_primary_stake,
            nft_holders_share=nft_holders_share,
            initial_redemption_fee=initial_redemption_fee,
            is_validator_id_switchable=is_validator_id_switchable,
            unit_backing=unit_backing,
            redemption_fee_duration=redemption_fee_duration,
            proposal_quorum=proposal_quorum,
            creator_royalties=creator_royalties,
            governance_expiration_time=governance_expiration_time,
            rarities=rarities,
            rarity_names=rarity_names,
            twitter_handle=twitter_handle,
            discord_invite=discord_invite,
            validator_name=validator_name,
            collection_uri=collection_uri,
            website=website,
            default_uri=default_uri,
            log_level=log_level,
        )
    )
    transaction = Transaction()
    # print(data)
    transaction.add(
        ComputeBudgetInstruction().set_compute_unit_limit(300_000, payer_keypair.pubkey)
    )
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )

    try:
        t_dets = await sign_and_send_tx(
            transaction, client, payer_keypair, skip_preflight=False
        )
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def mint_nft(
    payer_keypair: KeypairInput,
    mint_keypair: KeypairInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    mint_authority_pubkey, _mint_authority_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_MINT_AUTHORITY_KEY, "UTF-8")], get_program_id()
    )
    collection_mint_pubkey, _collection_mint_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_NFT_COLLECTION_KEY, "UTF-8")], get_program_id()
    )
    pd_pool_pubkey, _pd_pool_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.PD_POOL_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(
        payer_keypair.pubkey, mint_keypair.pubkey
    )
    metaplex_program_id = Pubkey.from_string(
        "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    )
    metadata_pda, _metadata_pda_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(mint_keypair.pubkey)],
        metaplex_program_id,
    )
    collection_master_edition_pda, _master_edition_bump = Pubkey.find_program_address(
        [
            b"metadata",
            bytes(metaplex_program_id),
            bytes(collection_mint_pubkey),
            b"edition",
        ],
        metaplex_program_id,
    )
    mint_edition_pda, _mint_edition_bump = Pubkey.find_program_address(
        [
            b"metadata",
            bytes(metaplex_program_id),
            bytes(mint_keypair.pubkey),
            b"edition",
        ],
        metaplex_program_id,
    )
    collection_account_pda, _collection_account_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(collection_mint_pubkey)],
        metaplex_program_id,
    )
    nft_account_pubkey, _nft_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint_keypair.pubkey)],
        get_program_id(),
    )
    ingl_config_pubkey, _ingl_config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    uri_account_pubkey, _uri_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.URIS_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    mint_account_meta = AccountMeta(mint_keypair.pubkey, True, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    mint_authority_meta = AccountMeta(mint_authority_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    sysvar_rent_account_meta = AccountMeta(solders.sysvar.RENT, False, False)
    system_program_meta = AccountMeta(system_program.ID, False, False)
    token_metadata_meta = AccountMeta(metadata_pda, False, True)
    metadata_program_id = AccountMeta(metaplex_program_id, False, False)
    associated_program_meta = AccountMeta(
        spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False
    )
    nft_account_meta = AccountMeta(nft_account_pubkey, False, True)
    collection_master_edition_meta = AccountMeta(
        collection_master_edition_pda, False, True
    )
    mint_edition_meta = AccountMeta(mint_edition_pda, False, True)
    collection_mint_meta = AccountMeta(collection_mint_pubkey, False, True)
    collection_account_meta = AccountMeta(collection_account_pda, False, True)
    ingl_config_meta = AccountMeta(ingl_config_pubkey, False, False)
    uri_account_meta = AccountMeta(uri_account_pubkey, False, True)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)

    accounts = [
        payer_account_meta,
        mint_account_meta,
        mint_authority_meta,
        mint_associated_meta,
        spl_program_meta,
        sysvar_rent_account_meta,
        system_program_meta,
        token_metadata_meta,
        pd_pool_meta,
        nft_account_meta,
        collection_master_edition_meta,
        mint_edition_meta,
        collection_mint_meta,
        collection_account_meta,
        ingl_config_meta,
        uri_account_meta,
        general_account_meta,
        system_program_meta,
        spl_program_meta,
        system_program_meta,
        spl_program_meta,
        associated_program_meta,
        spl_program_meta,
        metadata_program_id,
        metadata_program_id,
        spl_program_meta,
        metadata_program_id,
    ]

    instruction_data = build_instruction(
        InstructionEnum.enum.MintNft(
            switchboard_state_bump=0, permission_bump=0, log_level=log_level
        )
    )
    transaction = Transaction()
    transaction.add(
        ComputeBudgetInstruction().set_compute_unit_limit(400_000, payer_keypair.pubkey)
    )
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(
            transaction, client, payer_keypair, mint_keypair
        )
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def delegate_nft(
    payer_keypair: KeypairInput,
    mint_pubkey: PubkeyInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    nft_account_pubkey, _nft_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint_pubkey.pubkey)],
        get_program_id(),
    )
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(
        payer_keypair.pubkey, mint_pubkey.pubkey
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.pubkey, False, False)
    nft_account_meta = AccountMeta(nft_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, False)
    config_account_meta = AccountMeta(
        pubkey=config_account_pubkey, is_signer=False, is_writable=False
    )
    general_account_meta = AccountMeta(
        pubkey=general_account_pubkey, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        mint_account_meta,
        nft_account_meta,
        mint_associated_meta,
        general_account_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(
        InstructionEnum.enum.DelegateNFT(log_level=log_level)
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def undelegate_nft(
    payer_keypair: KeypairInput,
    mint_pubkey: PubkeyInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    nft_account_pubkey, _nft_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint_pubkey.pubkey)],
        get_program_id(),
    )
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(
        payer_keypair.pubkey, mint_pubkey.pubkey
    )
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    expected_vote_pubkey = Pubkey(config_data.vote_account)

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.pubkey, False, False)
    nft_account_meta = AccountMeta(nft_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, False)
    config_account_meta = AccountMeta(
        pubkey=config_account_pubkey, is_signer=False, is_writable=False
    )
    general_account_meta = AccountMeta(
        pubkey=general_account_pubkey, is_signer=False, is_writable=True
    )

    vote_account_meta = AccountMeta(expected_vote_pubkey, False, False)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, False)
    system_program_meta = AccountMeta(system_program.ID, False, False)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        config_account_meta,
        mint_account_meta,
        nft_account_meta,
        mint_associated_meta,
        general_account_meta,
        system_program_meta,
        authorized_withdrawer_meta,
    ] + interested_proposals_account_metas

    # print(accounts)
    instruction_data = build_instruction(
        InstructionEnum.enum.UnDelegateNFT(
            log_level=log_level,
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def create_vote_account(
    validator_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    expected_vote_pubkey, _expected_vote_pubkey_nonce = Pubkey.find_program_address(
        [bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    expected_stake_key, _expected_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    pd_pool_account_pubkey, _pd_pool_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.PD_POOL_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )

    print(f"Vote_Account: {expected_vote_pubkey}")

    rent_account_meta = AccountMeta(solders.sysvar.RENT, False, False)
    sysvar_clock_meta = AccountMeta(solders.sysvar.CLOCK, False, False)
    validator_meta = AccountMeta(validator_keypair.pubkey, True, True)
    vote_account_meta = AccountMeta(expected_vote_pubkey, False, True)
    sys_program_meta = AccountMeta(system_program.ID, False, False)
    vote_program_meta = AccountMeta(ingl_constants.VOTE_PROGRAM_ID, False, False)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)
    config_account_meta = AccountMeta(config_account_pubkey, False, True)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    pd_pool_account_meta = AccountMeta(pd_pool_account_pubkey, False, False)
    stake_history_meta = AccountMeta(STAKE_HISTORY, False, False)
    stake_config_meta = AccountMeta(
        ingl_constants.STAKE_CONFIG_PROGRAM_ID, False, False
    )

    accounts = [
        validator_meta,
        vote_account_meta,
        rent_account_meta,
        sysvar_clock_meta,
        spl_program_meta,
        stake_account_meta,
        config_account_meta,
        general_account_meta,
        pd_pool_account_meta,
        stake_history_meta,
        stake_config_meta,
        sys_program_meta,
        vote_program_meta,
        vote_program_meta,
        sys_program_meta,
        stake_program_meta,
    ]

    data = InstructionEnum.build(
        InstructionEnum.enum.CreateVoteAccount(
            log_level=log_level,
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, validator_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def init_rebalance(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    expected_stake_key, _expected_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_stake_key, _t_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_withdraw_key, _t_withdraw_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_WITHDRAW_KEY, "UTF-8")], get_program_id()
    )
    pd_pool_pubkey, _pd_pool_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.PD_POOL_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )


async def init_rebalance(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    expected_stake_key, _expected_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_stake_key, _t_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_withdraw_key, _t_withdraw_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_WITHDRAW_KEY, "UTF-8")], get_program_id()
    )
    pd_pool_pubkey, _pd_pool_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.PD_POOL_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )

    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    expected_vote_pubkey = Pubkey(config_data.vote_account)

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    rent_account_meta = AccountMeta(solders.sysvar.RENT, False, False)
    sysvar_clock_meta = AccountMeta(solders.sysvar.CLOCK, False, False)
    sys_program_meta = AccountMeta(system_program.ID, False, False)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    t_stake_meta = AccountMeta(t_stake_key, False, True)
    t_withdraw_meta = AccountMeta(t_withdraw_key, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)
    vote_account_meta = AccountMeta(expected_vote_pubkey, False, True)
    stake_history_meta = AccountMeta(STAKE_HISTORY, False, False)
    stake_config_meta = AccountMeta(
        ingl_constants.STAKE_CONFIG_PROGRAM_ID, False, False
    )
    config_account_meta = AccountMeta(config_account_pubkey, False, False)

    accounts = [
        payer_account_meta,
        t_stake_meta,
        pd_pool_meta,
        general_account_meta,
        sysvar_clock_meta,
        rent_account_meta,
        stake_account_meta,
        t_withdraw_meta,
        vote_account_meta,
        stake_history_meta,
        stake_config_meta,
        config_account_meta,
        sys_program_meta,
        stake_program_meta,
        sys_program_meta,
        sys_program_meta,
        stake_program_meta,
        stake_program_meta,
    ]
    # print(accounts)
    data = InstructionEnum.build(
        InstructionEnum.enum.InitRebalance(
            log_level=log_level,
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def finalize_rebalance(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    expected_stake_key, _expected_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_stake_key, _t_stake_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_STAKE_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    t_withdraw_key, _t_withdraw_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.T_WITHDRAW_KEY, "UTF-8")], get_program_id()
    )
    pd_pool_pubkey, _pd_pool_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.PD_POOL_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )

    data = await client.get_account_info(config_account_pubkey)
    validator_id = Pubkey(ValidatorConfig.parse(data.value.data).validator_id)
    print(f"Validator_Id: {validator_id}")

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    sysvar_clock_meta = AccountMeta(solders.sysvar.CLOCK, False, False)
    validator_meta = AccountMeta(validator_id, False, True)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    t_stake_meta = AccountMeta(t_stake_key, False, True)
    t_withdraw_meta = AccountMeta(t_withdraw_key, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)
    sysvar_stake_history_meta = AccountMeta(solders.sysvar.STAKE_HISTORY, False, False)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    config_account_meta = AccountMeta(config_account_pubkey, False, False)
    system_program_meta = AccountMeta(solders.system_program.ID, False, False)

    accounts = [
        payer_account_meta,
        validator_meta,
        t_stake_meta,
        pd_pool_meta,
        general_account_meta,
        sysvar_clock_meta,
        stake_account_meta,
        t_withdraw_meta,
        sysvar_stake_history_meta,
        config_account_meta,
        stake_program_meta,
        system_program_meta,
    ]

    data = InstructionEnum.build(
        InstructionEnum.enum.FinalizeRebalance(
            log_level=log_level,
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def process_rewards(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    ingl_team_account_pubkey = Pubkey.from_string(
        "Team111111111111111111111111111111111111111"
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )


async def process_rewards(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    ingl_team_account_pubkey = Pubkey.from_string(
        "Team111111111111111111111111111111111111111"
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    vote_account_key = Pubkey(config_data.vote_account)
    validator_id = Pubkey(config_data.validator_id)
    print(f"Validator_Id: {validator_id}")

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    validator_meta = AccountMeta(validator_id, False, True)
    vote_account_meta = AccountMeta(vote_account_key, False, True)
    sys_program_meta = AccountMeta(system_program.ID, False, False)
    vote_program_meta = AccountMeta(ingl_constants.VOTE_PROGRAM_ID, False, False)
    mint_authority_meta = AccountMeta(ingl_team_account_pubkey, False, True)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)
    config_account_meta = AccountMeta(config_account_pubkey, False, False)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)

    accounts = [
        payer_account_meta,
        validator_meta,
        vote_account_meta,
        authorized_withdrawer_meta,
        config_account_meta,
        general_account_meta,
        mint_authority_meta,
        vote_program_meta,
        sys_program_meta,
        sys_program_meta,
        sys_program_meta,
    ]
    # print(accounts)
    config_data = InstructionEnum.build(
        InstructionEnum.enum.ProcessRewards(
            log_level=log_level,
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=config_data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def nft_withdraw(
    payer_keypair: KeypairInput,
    mints: List[Pubkey],
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [
            bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8"),
            bytes(vote_account_id.pubkey),
        ],
        get_program_id(),
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )


async def nft_withdraw(
    payer_keypair: KeypairInput,
    mints: List[Pubkey],
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [
            bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8"),
            bytes(vote_account_id.pubkey),
        ],
        get_program_id(),
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )

    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    vote_account_id = Pubkey(config_data.vote_account)

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    vote_account_meta = AccountMeta(vote_account_id, False, True)
    sys_program_meta = AccountMeta(system_program.ID, False, False)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        general_account_meta,
        authorized_withdrawer_meta,
        sys_program_meta,
    ]

    for mint_pubkey in mints:
        mint_associated_account_pubkey = (
            assoc_instructions.get_associated_token_address(
                payer_keypair.pubkey, mint_pubkey.pubkey
            )
        )
        accounts.append(AccountMeta(mint_associated_account_pubkey, False, False))
        accounts.append(AccountMeta(mint_pubkey.pubkey, False, False))
        gem_account_pubkey, _gem_account_bump = Pubkey.find_program_address(
            [
                bytes(ingl_constants.GEM_ACCOUNT_CONST, "UTF-8"),
                bytes(mint_pubkey.pubkey),
            ],
            get_program_id(),
        )
        accounts.append(AccountMeta(gem_account_pubkey, False, True))

    accounts.append(sys_program_meta)
    # print(accounts)
    data = InstructionEnum.build(
        InstructionEnum.enum.NFTWithdraw(log_level=log_level, cnt=len(mints))
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def init_governance(
    payer_keypair: KeypairInput,
    mint: PubkeyInput,
    client: AsyncClient,
    title: str,
    description: str,
    governance_type: Optional[GovernanceType.enum] = None,
    config_account_type: Optional[ConfigAccountType.enum] = None,
    vote_account_governance: Optional[VoteAccountGovernance.enum] = None,
    log_level: int = 0,
) -> str:
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    nft_account_data_pubkey, _nft_account_data_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint.pubkey)],
        get_program_id(),
    )
    associated_account_key = assoc_instructions.get_associated_token_address(
        payer_keypair.pubkey, mint.pubkey
    )

    data = await client.get_account_info(general_account_pubkey)
    proposal_numeration = GeneralData.parse(data.value.data).proposal_numeration
    print(f"proposal_numeration: {proposal_numeration}")

    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    vote_account_key = Pubkey(config_data.vote_account)

    proposal_pubkey, _proposal_bump = Pubkey.find_program_address(
        [
            bytes(ingl_constants.INGL_PROPOSAL_KEY, "UTF-8"),
            (proposal_numeration).to_bytes(4, "big"),
        ],
        get_program_id(),
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    vote_account_meta = AccountMeta(
        pubkey=vote_account_key, is_signer=False, is_writable=True
    )
    proposal_account_meta = AccountMeta(
        pubkey=proposal_pubkey, is_signer=False, is_writable=True
    )
    general_account_meta = AccountMeta(
        pubkey=general_account_pubkey, is_signer=False, is_writable=True
    )
    mint_account_meta = AccountMeta(
        pubkey=mint.pubkey, is_signer=False, is_writable=False
    )
    associated_account_meta = AccountMeta(
        pubkey=associated_account_key, is_signer=False, is_writable=False
    )
    nft_account_data_meta = AccountMeta(
        pubkey=nft_account_data_pubkey, is_signer=False, is_writable=False
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_pubkey, is_signer=False, is_writable=False
    )

    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    accounts = [
        payer_account_meta,
        vote_account_meta,
        proposal_account_meta,
        general_account_meta,
        mint_account_meta,
        associated_account_meta,
        nft_account_data_meta,
        config_account_meta,
    ]

    instruction_data = build_instruction(
        InstructionEnum.enum.InitGovernance(),
        title=title,
        description=description,
        governance_type=governance_type,
        config_account_type=config_account_type,
        vote_account_governance=vote_account_governance,
        log_level=log_level,
    )
    print("instruction_data: ", instruction_data)
    if instruction_data[1] == 1:
        buffer_account_key = Pubkey(instruction_data[2:34])
        buffer_account_meta = AccountMeta(
            pubkey=buffer_account_key, is_signer=False, is_writable=True
        )
        print("buffer_account_key: ", buffer_account_key)
        accounts.append(buffer_account_meta)

    accounts += [
        system_program_meta,
    ]

    # print(accounts)
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def vote_governance(
    payer_keypair: KeypairInput,
    vote: Bool,
    proposal_numeration: int,
    mints: List[Pubkey],
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    proposal_pubkey, _proposal_account_bump = Pubkey.find_program_address(
        [
            bytes(ingl_constants.INGL_PROPOSAL_KEY, "UTF-8"),
            (proposal_numeration).to_bytes(4, "big"),
        ],
        get_program_id(),
    )

    print(
        f"Proposal_Account: {proposal_pubkey}, Vote: {'Approve' if vote else 'Dissaprove'} "
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    proposal_account_meta = AccountMeta(
        pubkey=proposal_pubkey, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    accounts = [
        payer_account_meta,
        proposal_account_meta,
    ]

    for mint in mints:
        associated_account_key = assoc_instructions.get_associated_token_address(
            payer_keypair.pubkey, mint
        )
        nft_account_pubkey, _nft_account_bump = Pubkey.find_program_address(
            [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint)],
            get_program_id(),
        )

        nft_account_meta = AccountMeta(
            pubkey=nft_account_pubkey, is_signer=False, is_writable=True
        )
        mint_account_meta = AccountMeta(pubkey=mint, is_signer=False, is_writable=False)
        associated_account_meta = AccountMeta(
            pubkey=associated_account_key, is_signer=False, is_writable=False
        )
        accounts += [
            nft_account_meta,
            mint_account_meta,
            associated_account_meta,
        ]
    accounts.append(system_program_meta)

    # print(accounts)
    instruction_data = build_instruction(
        InstructionEnum.enum.VoteGovernance(
            log_level=log_level,
            numeration=proposal_numeration,
            vote=vote,
            cnt=len(mints),
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def finalize_governance(
    payer_keypair: KeypairInput,
    proposal_numeration: int,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    proposal_account_key, _proposal_account_bump = Pubkey.find_program_address(
        [
            bytes(ingl_constants.INGL_PROPOSAL_KEY, "UTF-8"),
            (proposal_numeration).to_bytes(4, "big"),
        ],
        get_program_id(),
    )
    config_account_key, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_key, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    print(f"Proposal_Account: {proposal_account_key}")

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    sysvar_rent_account_meta = AccountMeta(
        pubkey=RENT, is_signer=False, is_writable=False
    )
    sysvar_clock_account_meta = AccountMeta(
        pubkey=CLOCK, is_signer=False, is_writable=False
    )
    proposal_account_meta = AccountMeta(
        pubkey=proposal_account_key, is_signer=False, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    general_account_meta = AccountMeta(
        pubkey=general_account_key, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        sysvar_rent_account_meta,
        sysvar_clock_account_meta,
        proposal_account_meta,
        config_account_meta,
        general_account_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(
        InstructionEnum.enum.FinalizeGovernance(
            log_level=log_level, numeration=proposal_numeration
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def execute_governance(
    payer_keypair: KeypairInput,
    proposal_numeration: int,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    proposal_account_key, _proposal_account_bump = Pubkey.find_program_address(
        [
            bytes(ingl_constants.INGL_PROPOSAL_KEY, "UTF-8"),
            (proposal_numeration).to_bytes(4, "big"),
        ],
        get_program_id(),
    )
    config_account_key, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_key, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    print(f"Proposal_Account: {proposal_account_key}")

    proposal_data = await client.get_account_info(proposal_account_key)
    proposal_data = proposal_data.value.data

    # payer is the validator ID.
    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    sysvar_rent_account_meta = AccountMeta(
        pubkey=RENT, is_signer=False, is_writable=False
    )
    sysvar_clock_account_meta = AccountMeta(
        pubkey=CLOCK, is_signer=False, is_writable=False
    )
    proposal_account_meta = AccountMeta(
        pubkey=proposal_account_key, is_signer=False, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    general_account_meta = AccountMeta(
        pubkey=general_account_key, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        sysvar_clock_account_meta,
        proposal_account_meta,
        config_account_meta,
        general_account_meta,
    ]

    loc = 4 + 4 + 1
    if proposal_data[loc] == 1:
        loc += 1 + 4
    else:
        loc += 1

    if proposal_data[loc] == 1:
        loc += 1 + 1
    else:
        loc += 1

    loc += 1

    title_len = int.from_bytes(proposal_data[loc : loc + 4], "big")
    loc += 4
    loc += title_len

    desc_len = int.from_bytes(proposal_data[loc : loc + 4], "big")
    loc += 4
    loc += desc_len

    num_votes = int.from_bytes(proposal_data[loc : loc + 4], "big")
    loc += 4
    loc += num_votes * 5
    governance_type = proposal_data[loc]
    loc += 1
    if governance_type == 0:
        pass
    elif governance_type == 1:
        buffer_account_key = Pubkey(proposal_data[loc : loc + 32])
        programdata_key, _programdata_bump = Pubkey.find_program_address(
            [bytes(get_program_id())], ingl_constants.BPF_LOADER_UPGRADEABLE
        )
        upgrade_authority_key, _upgrade_authority_bump = Pubkey.find_program_address(
            [
                bytes(ingl_constants.INGL_PROGRAM_AUTHORITY_KEY, "UTF-8"),
                bytes(get_program_id()),
            ],
            get_program_id(),
        )

        upgraded_program_meta = AccountMeta(
            pubkey=get_program_id(), is_signer=False, is_writable=False
        )
        buffer_account_meta = AccountMeta(
            pubkey=buffer_account_key, is_signer=False, is_writable=True
        )
        programdata_account_meta = AccountMeta(
            pubkey=programdata_key, is_signer=False, is_writable=True
        )
        upgrade_authority_account_meta = AccountMeta(
            pubkey=upgrade_authority_key, is_signer=False, is_writable=True
        )

        accounts += [
            upgraded_program_meta,
            buffer_account_meta,
            payer_account_meta,
            programdata_account_meta,
            upgrade_authority_account_meta,
            sysvar_rent_account_meta,
            sysvar_clock_account_meta,
        ]
    elif governance_type == 2:
        vote_account_governance_type = proposal_data[loc]
        loc += 1
        vote_account_key, _vote_account_bump = Pubkey.find_program_address(
            [
                bytes(ingl_constants.INGL_VOTE_KEY, "UTF-8"),
            ],
            get_program_id(),
        )
        (
            authorized_withdrawer_key,
            _authorized_withdrawer_bump,
        ) = Pubkey.find_program_address(
            [
                bytes(ingl_constants.INGL_VOTE_AUTHORIZED_WITHDRAWER_KEY, "UTF-8"),
            ],
            get_program_id(),
        )

        vote_account_meta = AccountMeta(
            pubkey=vote_account_key, is_signer=False, is_writable=True
        )
        authorized_withdrawer_account_meta = AccountMeta(
            pubkey=authorized_withdrawer_key, is_signer=False, is_writable=False
        )

        accounts += [
            vote_account_meta,
            authorized_withdrawer_account_meta,
        ]

        if vote_account_governance_type == 0:
            accounts.append(sysvar_clock_account_meta)
            accounts.append(payer_account_meta)

    # print(accounts)
    instruction_data = build_instruction(
        InstructionEnum.enum.ExecuteGovernance(
            log_level=log_level, numeration=proposal_numeration
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def reset_uris(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )
    # payer is the validator id address.
    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    uris_account_key, uris_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_URIS_ACCOUNT_KEY, "UTF-8")], get_program_id()
    )

    uris_account_meta = AccountMeta(
        pubkey=uris_account_key, is_signer=False, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        uris_account_meta,
        system_program_meta,
    ]

    instruction_data = build_instruction(
        InstructionEnum.enum.ResetUris(log_level=log_level)
    )
    transaction = Transaction()
    transaction.add(
        Instruction(
            accounts=accounts, program_id=get_program_id(), data=instruction_data
        )
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


def upload_uris(
    payer_keypair: KeypairInput,
    upload_authority: KeypairInput,
    uris: List[str],
    rarity: int,
    client: Client,
    log_level: int = 0,
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    uris_account_key, _config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.URIS_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )
    uris_account_meta = AccountMeta(
        pubkey=uris_account_key, is_signer=False, is_writable=True
    )
    upload_authority_account_meta = AccountMeta(
        pubkey=upload_authority.pubkey, is_signer=True, is_writable=False
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        uris_account_meta,
        upload_authority_account_meta,
        system_program_meta,
    ]

    t_dets = None
    try:
        instruction_data = build_instruction(
            InstructionEnum.enum.UploadUris(
                uris=uris, rarity=rarity, log_level=log_level
            )
        )
        transaction = Transaction()
        transaction.add(
            ComputeBudgetInstruction().set_compute_unit_limit(
                1_000_000, payer_keypair.pubkey
            )
        )
        transaction.add(
            Instruction(
                accounts=accounts, program_id=get_program_id(), data=instruction_data
            )
        )
        t_dets = client.send_transaction(transaction, payer_keypair.keypair)
        return t_dets
    except Exception as e:
        print(t_dets, e)
        raise e


async def reset_uris(
    payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    uris_account_key, _config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.URIS_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )
    uris_account_meta = AccountMeta(
        pubkey=uris_account_key, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        uris_account_meta,
        system_program_meta,
    ]

    t_dets = None
    try:
        instruction_data = build_instruction(
            InstructionEnum.enum.ResetUris(log_level=log_level)
        )
        transaction = Transaction()
        transaction.add(
            ComputeBudgetInstruction().set_compute_unit_limit(
                1_000_000, payer_keypair.pubkey
            )
        )
        transaction.add(
            Instruction(
                accounts=accounts, program_id=get_program_id(), data=instruction_data
            )
        )
        t_dets = await client.send_transaction(transaction, payer_keypair.keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        print(t_dets, e)
        raise e


async def init_registry(
    payer_keypair: KeypairInput,
    client: AsyncClient,
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [b"config"], ingl_constants.REGISTRY_PROGRAM
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        system_program_meta,
    ]

    t_dets = None
    try:
        instruction_data = RegistryEnum.build(RegistryEnum.enum.InitConfig())
        transaction = Transaction()
        transaction.add(
            Instruction(
                accounts=accounts,
                program_id=ingl_constants.REGISTRY_PROGRAM,
                data=instruction_data,
            )
        )
        t_dets = await client.send_transaction(transaction, payer_keypair.keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        print(t_dets, e)
        raise e


async def reset_registry(
    payer_keypair: KeypairInput,
    client: AsyncClient,
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [b"config"], ingl_constants.REGISTRY_PROGRAM
    )

    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )
    storage_account_key, _config_account_bump = Pubkey.find_program_address(
        [b"storage"],
        ingl_constants.REGISTRY_PROGRAM,
    )
    name_storage_key, _name_storage_bump = Pubkey.find_program_address(
        [b"name_storage"],
        ingl_constants.REGISTRY_PROGRAM,
    )
    marketplace_storage_key, _marketplace_storage_bump = Pubkey.find_program_address(
        [b"marketplace_storage"],
        ingl_constants.REGISTRY_PROGRAM,
    )

    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )

    name_storage_meta = AccountMeta(
        pubkey=name_storage_key, is_signer=False, is_writable=True
    )

    marketplace_storage_meta = AccountMeta(
        pubkey=marketplace_storage_key, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        storage_account_meta,
        name_storage_meta,
        marketplace_storage_meta,
        system_program_meta,
    ]

    t_dets = None
    try:
        instruction_data = RegistryEnum.build(RegistryEnum.enum.Reset())
        transaction = Transaction()
        transaction.add(
            Instruction(
                accounts=accounts,
                program_id=ingl_constants.REGISTRY_PROGRAM,
                data=instruction_data,
            )
        )
        t_dets = await client.send_transaction(transaction, payer_keypair.keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        print(t_dets, e)
        raise e


async def register_program(
    payer_keypair: KeypairInput,
    program_key: Pubkey,
    client: AsyncClient,
) -> str:
    config_account_key, _config_bump = Pubkey.find_program_address(
        [b"config"], ingl_constants.REGISTRY_PROGRAM
    )
    payer_account_meta = AccountMeta(
        pubkey=payer_keypair.pubkey, is_signer=True, is_writable=True
    )
    config_account_meta = AccountMeta(
        pubkey=config_account_key, is_signer=False, is_writable=True
    )
    registered_program_meta = AccountMeta(
        pubkey=program_key, is_signer=False, is_writable=False
    )
    team_account_meta = AccountMeta(
        pubkey=ingl_constants.TEAM_ADDRESS, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    config_data = await client.get_account_info(config_account_key)
    config_data = RegistryConfig.parse(config_data.value.data)
    storage_account_key, _config_account_bump = Pubkey.find_program_address(
        [b"storage", (config_data.validator_numeration // 625).to_bytes(4, "big")],
        ingl_constants.REGISTRY_PROGRAM,
    )
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )

    accounts = [
        payer_account_meta,
        config_account_meta,
        registered_program_meta,
        team_account_meta,
        storage_account_meta,
        system_program_meta,
    ]

    t_dets = None
    try:
        instruction_data = RegistryEnum.build(RegistryEnum.enum.AddProgram(name=name))
        transaction = Transaction()
        transaction.add(
            Instruction(
                accounts=accounts,
                program_id=ingl_constants.REGISTRY_PROGRAM,
                data=instruction_data,
            )
        )
        t_dets = await client.send_transaction(transaction, payer_keypair.keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        print(t_dets, e)
        raise e


async def fractionalize_existing(
    payer_keypair: KeypairInput,
    authorized_withdrawer: KeypairInput,
    upgrade_authority: KeypairInput,
    vote_account_pubkey: PubkeyInput,
    validator_pubkey: PubkeyInput,
    init_commission: int,
    max_primary_stake: int,
    nft_holders_share: int,
    initial_redemption_fee: int,
    is_validator_id_switchable: bool,
    unit_backing: int,
    redemption_fee_duration: int,
    proposal_quorum: int,
    creator_royalties: int,
    governance_expiration_time: int,
    rarities: List[int],
    rarity_names: List[str],
    twitter_handle: str,
    discord_invite: str,
    validator_name: str,
    collection_uri: str,
    website: str,
    default_uri: str,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    mint_pubkey, _mint_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_NFT_COLLECTION_KEY, "UTF-8")], get_program_id()
    )
    mint_authority_pubkey, _mint_authority_pubkey_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_MINT_AUTHORITY_KEY, "UTF-8")], get_program_id()
    )
    (
        collection_holder_pubkey,
        _collection_holder_pubkey_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.COLLECTION_HOLDER_KEY, "UTF-8")], get_program_id()
    )
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(
        collection_holder_pubkey, mint_pubkey
    )
    metaplex_program_id = Pubkey.from_string(
        "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    )
    metadata_pda, _metadata_pda_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey)],
        metaplex_program_id,
    )
    master_edition_pda, _master_edition_bump = Pubkey.find_program_address(
        [b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey), b"edition"],
        metaplex_program_id,
    )
    ingl_config_pubkey, _ingl_config_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], get_program_id()
    )
    general_account_pubkey, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )
    uris_account_pubkey, _uris_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.URIS_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    (
        registry_program_config_key,
        _registry_program_config_bump,
    ) = Pubkey.find_program_address([b"config"], ingl_constants.REGISTRY_PROGRAM_ID)

    registry_config_account = await client.get_account_info(registry_program_config_key)
    registry_config_data = RegistryConfig.parse(registry_config_account.value.data)
    storage_numeration = registry_config_data.validator_numeration // 625
    name_storage_numeration = registry_config_data.validator_numeration // 1666
    storage_key, _storage_bump = Pubkey.find_program_address(
        [b"storage", storage_numeration.to_bytes(4, "big")],
        ingl_constants.REGISTRY_PROGRAM_ID,
    )

    (
        pda_authorized_withdrawer,
        _pda_authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_AUTHORIZED_WITHDRAWER_KEY, "UTF-8")],
        get_program_id(),
    )

    programdata_key, _programdata_bump = Pubkey.find_program_address(
        [bytes(get_program_id())], ingl_constants.BPF_LOADER_UPGRADEABLE
    )

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    collection_holder_meta = AccountMeta(collection_holder_pubkey, False, True)
    mint_account_meta = AccountMeta(mint_pubkey, False, True)
    mint_authority_meta = AccountMeta(mint_authority_pubkey, False, False)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    sysvar_rent_account_meta = AccountMeta(solders.sysvar.RENT, False, False)
    system_program_meta = AccountMeta(system_program.ID, False, False)
    token_metadata_meta = AccountMeta(metadata_pda, False, True)
    metadata_program_id = AccountMeta(metaplex_program_id, False, False)
    associated_program_meta = AccountMeta(
        spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False
    )
    edition_meta = AccountMeta(master_edition_pda, False, True)
    ingl_config_meta = AccountMeta(ingl_config_pubkey, False, True)
    general_account_meta = AccountMeta(general_account_pubkey, False, True)
    uris_account_meta = AccountMeta(uris_account_pubkey, False, True)
    validator_account_meta = AccountMeta(validator_pubkey.pubkey, False, True)
    registry_program_config_meta = AccountMeta(registry_program_config_key, False, True)
    program_meta = AccountMeta(get_program_id(), False, False)
    team_account_meta = AccountMeta(ingl_constants.TEAM_ACCOUNT_KEY, False, True)
    storage_account_meta = AccountMeta(storage_key, False, True)
    registry_program_meta = AccountMeta(
        ingl_constants.REGISTRY_PROGRAM_ID, False, False
    )
    current_authorized_withdrawer_meta = AccountMeta(
        authorized_withdrawer.pubkey, True, False
    )
    pda_authorized_withdrawer_meta = AccountMeta(
        pda_authorized_withdrawer, False, False
    )
    vote_account_meta = AccountMeta(vote_account_pubkey.pubkey, False, True)
    sysvar_clock_meta = AccountMeta(solders.sysvar.CLOCK, False, False)
    this_program_data_meta = AccountMeta(
        pubkey=programdata_key, is_signer=False, is_writable=False
    )
    current_upgrade_authority_meta = AccountMeta(upgrade_authority, True, False)

    accounts = [
        payer_account_meta,
        ingl_config_meta,
        general_account_meta,
        uris_account_meta,
        sysvar_rent_account_meta,
        validator_account_meta,
        collection_holder_meta,
        mint_account_meta,
        mint_authority_meta,
        mint_associated_meta,
        token_metadata_meta,
        edition_meta,
        spl_program_meta,
        system_program_meta,
        this_program_data_meta,
        current_upgrade_authority_meta,
        current_authorized_withdrawer_meta,
        pda_authorized_withdrawer_meta,
        vote_account_meta,
        sysvar_clock_meta,
        program_meta,
        team_account_meta,
        storage_account_meta,
        system_program_meta,
        associated_program_meta,
        spl_program_meta,
        metadata_program_id,
        registry_program_meta,
    ]
    # print(accounts)
    data = build_instruction(
        InstructionEnum.enum.FractionalizeExisting(
            init_commission=init_commission,
            max_primary_stake=max_primary_stake,
            nft_holders_share=nft_holders_share,
            initial_redemption_fee=initial_redemption_fee,
            is_validator_id_switchable=is_validator_id_switchable,
            unit_backing=unit_backing,
            redemption_fee_duration=redemption_fee_duration,
            proposal_quorum=proposal_quorum,
            creator_royalties=creator_royalties,
            governance_expiration_time=governance_expiration_time,
            name_storage_numeration=name_storage_numeration,
            rarities=rarities,
            rarity_names=rarity_names,
            twitter_handle=twitter_handle,
            discord_invite=discord_invite,
            validator_name=validator_name,
            collection_uri=collection_uri,
            website=website,
            default_uri=default_uri,
            log_level=log_level,
        )
    )
    transaction = Transaction()
    # print(data)
    transaction.add(
        ComputeBudgetInstruction().set_compute_unit_limit(400_000, payer_keypair.pubkey)
    )
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )

    try:
        t_dets = await sign_and_send_tx(
            transaction, client, payer_keypair, authorized_withdrawer
        )
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"Error: {e}"


async def inject_testing_data(
    payer_keypair: KeypairInput,
    mints: List[Pubkey],
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    (
        authorized_withdrawer_key,
        _authorized_withdrawer_bump,
    ) = Pubkey.find_program_address(
        [bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, "UTF-8")], get_program_id()
    )
    general_account_key, _general_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.GENERAL_ACCOUNT_SEED, "UTF-8")], get_program_id()
    )

    payer_account_meta = AccountMeta(payer_keypair.pubkey, True, True)
    general_account_meta = AccountMeta(general_account_key, False, True)
    sys_program_meta = AccountMeta(system_program.ID, False, False)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)

    accounts = [
        payer_account_meta,
        general_account_meta,
        authorized_withdrawer_meta,
    ]

    for mint_pubkey in mints:
        accounts.append(AccountMeta(mint_pubkey, False, False))
        nft_account_pubkey, _nft_account_bump = Pubkey.find_program_address(
            [bytes(ingl_constants.NFT_ACCOUNT_CONST, "UTF-8"), bytes(mint_pubkey)],
            get_program_id(),
        )
        accounts.append(AccountMeta(nft_account_pubkey, False, True))

    accounts.append(sys_program_meta)
    # print(accounts)
    data = InstructionEnum.build(
        InstructionEnum.enum.InjectTestingData(
            log_level=log_level, num_mints=len(mints)
        )
    )
    transaction = Transaction()
    transaction.add(
        Instruction(accounts=accounts, program_id=get_program_id(), data=data)
    )
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(
            tx_sig=t_dets.value,
            commitment="finalized",
            sleep_seconds=0.4,
            last_valid_block_height=None,
        )
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+get_explorer_suffix(get_network())}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return f"[warning]Error: {e}[/warning]"


# Market Processes are below:


async def process_list_validator(
    authorized_withdrawer: KeypairInput,
    current_upgrade_authority: KeypairInput,
    vote_account: PubkeyInput,
    authorized_withdrawer_cost: int,
    mediatable_date: int,
    secondary_items: List[dict],
    description: str,
    validator_name: str,
    validator_logo_url: str,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    pda_authorized_withdrawer_key, _pda_aw_bump = Pubkey.find_program_address(
        [ingl_constants.PDA_AUTHORIZED_WITHDRAWER_SEED], get_market_program_id()
    )
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )
    this_program_data_key, _this_program_data_bump = Pubkey.find_program_address(
        [bytes(get_market_program_id())], ingl_constants.BPF_LOADER_UPGRADEABLE
    )
    (
        pda_upgrade_authority_key,
        _pda_upgrade_authority_bump,
    ) = Pubkey.find_program_address(
        [ingl_constants.PDA_UPGRADE_AUTHORITY_SEED], get_market_program_id()
    )
    registry_storage_key, _registry_storage_bump = Pubkey.find_program_address(
        [ingl_constants.REGISTRY_STORAGE_SEED], ingl_constants.REGISTRY_PROGRAM
    )

    # Forming AccountMetas
    authorized_withdrawer_meta = AccountMeta(
        pubkey=authorized_withdrawer.pubkey, is_signer=True, is_writable=True
    )
    vote_account_meta = AccountMeta(
        pubkey=vote_account.pubkey, is_signer=False, is_writable=True
    )
    pda_authorized_withdrawer_meta = AccountMeta(
        pubkey=pda_authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    this_program_meta = AccountMeta(
        pubkey=get_market_program_id(), is_signer=False, is_writable=True
    )
    this_program_data_meta = AccountMeta(
        pubkey=this_program_data_key, is_signer=False, is_writable=True
    )
    current_upgrade_authority_meta = AccountMeta(
        pubkey=current_upgrade_authority.pubkey, is_signer=True, is_writable=False
    )
    pda_upgrade_authority_meta = AccountMeta(
        pubkey=pda_upgrade_authority_key, is_signer=False, is_writable=False
    )
    sysvar_clock_meta = AccountMeta(
        pubkey=solders.sysvar.CLOCK, is_signer=False, is_writable=False
    )
    team_account_meta = AccountMeta(
        pubkey=ingl_constants.TEAM_ADDRESS, is_signer=False, is_writable=True
    )
    registry_storage_meta = AccountMeta(
        pubkey=registry_storage_key, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )
    rent_sysvar_meta = AccountMeta(
        pubkey=solders.sysvar.RENT, is_signer=False, is_writable=False
    )
    vote_program_meta = AccountMeta(
        pubkey=ingl_constants.VOTE_PROGRAM_ID, is_signer=False, is_writable=False
    )
    bpf_loader_upgradeable_meta = AccountMeta(
        pubkey=ingl_constants.BPF_LOADER_UPGRADEABLE, is_signer=False, is_writable=False
    )
    register_program_meta = AccountMeta(
        pubkey=ingl_constants.REGISTRY_PROGRAM, is_signer=False, is_writable=False
    )

    account_metas = [
        authorized_withdrawer_meta,
        vote_account_meta,
        pda_authorized_withdrawer_meta,
        storage_account_meta,
        this_program_meta,
        this_program_data_meta,
        current_upgrade_authority_meta,
        pda_upgrade_authority_meta,
        sysvar_clock_meta,
        team_account_meta,
        registry_storage_meta,
        system_program_meta,
        rent_sysvar_meta,
        # programs listed below
        vote_program_meta,
        bpf_loader_upgradeable_meta,
        register_program_meta,
    ]
    # print(account_metas)

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.List(
                log_level=log_level,
                authorized_withdrawer_cost=authorized_withdrawer_cost,
                mediatable_date=mediatable_date,
                secondary_items=secondary_items,
                description=description,
                validator_name=validator_name,
                validator_logo_url=validator_logo_url,
            ),
            account_metas,
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(
        transaction, client, authorized_withdrawer, current_upgrade_authority
    )


async def process_delist_validator(
    authorized_withdrawer: KeypairInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    pda_authorized_withdrawer_key, _pda_aw_bump = Pubkey.find_program_address(
        [ingl_constants.PDA_AUTHORIZED_WITHDRAWER_SEED], get_market_program_id()
    )
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )
    this_program_data_key, _this_program_data_bump = Pubkey.find_program_address(
        [bytes(get_market_program_id())], ingl_constants.BPF_LOADER_UPGRADEABLE
    )
    (
        pda_upgrade_authority_key,
        _pda_upgrade_authority_bump,
    ) = Pubkey.find_program_address(
        [ingl_constants.PDA_UPGRADE_AUTHORITY_SEED], get_market_program_id()
    )

    storage_account_data = Storage.parse(
        (await client.get_account_info(storage_account_key)).value.data
    )
    vote_account_key = Pubkey(storage_account_data.vote_account)

    # Forming AccountMetas
    authorized_withdrawer_meta = AccountMeta(
        pubkey=authorized_withdrawer.pubkey, is_signer=True, is_writable=True
    )
    vote_account_meta = AccountMeta(
        pubkey=vote_account_key, is_signer=False, is_writable=True
    )
    pda_authorized_withdrawer_meta = AccountMeta(
        pubkey=pda_authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    this_program_meta = AccountMeta(
        pubkey=get_market_program_id(), is_signer=False, is_writable=True
    )
    this_program_data_meta = AccountMeta(
        pubkey=this_program_data_key, is_signer=False, is_writable=True
    )
    pda_upgrade_authority_meta = AccountMeta(
        pubkey=pda_upgrade_authority_key, is_signer=False, is_writable=False
    )
    sysvar_clock_meta = AccountMeta(
        pubkey=solders.sysvar.CLOCK, is_signer=False, is_writable=False
    )
    vote_program_meta = AccountMeta(
        pubkey=ingl_constants.VOTE_PROGRAM_ID, is_signer=False, is_writable=False
    )
    bpf_loader_upgradeable_meta = AccountMeta(
        pubkey=ingl_constants.BPF_LOADER_UPGRADEABLE, is_signer=False, is_writable=False
    )

    account_metas = [
        authorized_withdrawer_meta,
        vote_account_meta,
        pda_authorized_withdrawer_meta,
        storage_account_meta,
        this_program_meta,
        this_program_data_meta,
        pda_upgrade_authority_meta,
        sysvar_clock_meta,
        # programs listed below
        vote_program_meta,
        bpf_loader_upgradeable_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.Delist(log_level=log_level), account_metas
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(
        transaction, client, authorized_withdrawer
    )


async def process_buy_validator(
    payer: KeypairInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    pda_authorized_withdrawer_key, _pda_aw_bump = Pubkey.find_program_address(
        [ingl_constants.PDA_AUTHORIZED_WITHDRAWER_SEED], get_market_program_id()
    )
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )
    escrow_account_key, _escrow_bump = Pubkey.find_program_address(
        [ingl_constants.ESCROW_ACCOUNT_SEED], get_market_program_id()
    )

    storage_account_data = Storage.parse(
        (await client.get_account_info(storage_account_key)).value.data
    )
    vote_account_key = Pubkey(storage_account_data.vote_account)
    registered_authorized_withdrawer_key = Pubkey(
        storage_account_data.authorized_withdrawer
    )

    # Forming AccountMetas
    payer_meta = AccountMeta(pubkey=payer.pubkey, is_signer=True, is_writable=True)
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    registered_authorized_withdrawer_meta = AccountMeta(
        pubkey=registered_authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    vote_account_meta = AccountMeta(
        pubkey=vote_account_key, is_signer=False, is_writable=True
    )
    sysvar_clock_meta = AccountMeta(
        pubkey=solders.sysvar.CLOCK, is_signer=False, is_writable=False
    )
    pda_authorized_withdrawer_meta = AccountMeta(
        pubkey=pda_authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    escrow_account_meta = AccountMeta(
        pubkey=escrow_account_key, is_signer=False, is_writable=True
    )
    team_account_meta = AccountMeta(
        pubkey=ingl_constants.TEAM_ADDRESS, is_signer=False, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )
    vote_program_meta = AccountMeta(
        pubkey=ingl_constants.VOTE_PROGRAM_ID, is_signer=False, is_writable=False
    )

    account_metas = [
        payer_meta,
        storage_account_meta,
        registered_authorized_withdrawer_meta,
        vote_account_meta,
        sysvar_clock_meta,
        pda_authorized_withdrawer_meta,
        escrow_account_meta,
        team_account_meta,
        # programs listed below
        system_program_meta,
        vote_program_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.Buy(log_level=log_level), account_metas
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(transaction, client, payer)


async def process_withdraw_rewards(
    authorized_withdrawer: KeypairInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    pda_authorized_withdrawer_key, _pda_aw_bump = Pubkey.find_program_address(
        [ingl_constants.PDA_AUTHORIZED_WITHDRAWER_SEED], get_market_program_id()
    )
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )

    storage_account_data = Storage.parse(
        (await client.get_account_info(storage_account_key)).value.data
    )
    vote_account_key = Pubkey(storage_account_data.vote_account)

    # Forming AccountMetas
    authorized_withdrawer_meta = AccountMeta(
        pubkey=authorized_withdrawer.pubkey, is_signer=True, is_writable=True
    )
    vote_account_meta = AccountMeta(
        pubkey=vote_account_key, is_signer=False, is_writable=True
    )
    pda_authorized_withdrawer_meta = AccountMeta(
        pubkey=pda_authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    vote_program_meta = AccountMeta(
        pubkey=ingl_constants.VOTE_PROGRAM_ID, is_signer=False, is_writable=False
    )

    account_metas = [
        authorized_withdrawer_meta,
        vote_account_meta,
        pda_authorized_withdrawer_meta,
        storage_account_meta,
        # programs listed below
        vote_program_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.WithdrawRewards(log_level=log_level),
            account_metas,
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(
        transaction, client, authorized_withdrawer
    )


async def process_request_mediation(
    payer: KeypairInput,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )

    # Forming AccountMetas
    payer_meta = AccountMeta(pubkey=payer.pubkey, is_signer=True, is_writable=True)
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )

    account_metas = [
        payer_meta,
        storage_account_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.RequestMediation(log_level=log_level),
            account_metas,
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(transaction, client, payer)


async def process_mediate(
    payer: KeypairInput,
    mediation_shares: dict,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )

    escrow_account_key, _escrow_bump = Pubkey.find_program_address(
        [ingl_constants.ESCROW_SEED], get_market_program_id()
    )

    storage_account_data = Storage.parse(
        (await client.get_account_info(storage_account_key)).value.data
    )

    authorized_withdrawer_key = Pubkey(storage_account_data.authorized_withdrawer)
    buyer_key = Pubkey(storage_account_data.purchase.buyer)

    # Forming AccountMetas
    payer_meta = AccountMeta(pubkey=payer.pubkey, is_signer=True, is_writable=True)
    authorized_withdrawer_meta = AccountMeta(
        pubkey=authorized_withdrawer_key, is_signer=False, is_writable=True
    )
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    buyer_account_meta = AccountMeta(
        pubkey=buyer_key, is_signer=False, is_writable=True
    )
    escrow_account_meta = AccountMeta(
        pubkey=escrow_account_key, is_signer=False, is_writable=True
    )
    team_account_meta = AccountMeta(
        pubkey=ingl_constants.TEAM_ADDRESS, is_signer=False, is_writable=True
    )

    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    account_metas = [
        payer_meta,
        authorized_withdrawer_meta,
        storage_account_meta,
        buyer_account_meta,
        escrow_account_meta,
        team_account_meta,
        # programs listed below
        system_program_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.ProcessMediation(
                log_level=log_level, mediation_shares=mediation_shares
            ),
            account_metas,
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(transaction, client, payer)


async def process_validate_secondary_item_transfers(
    authorized_withdrawer: KeypairInput,
    item_index: int,
    client: AsyncClient,
    log_level: int = 0,
) -> str:
    storage_account_key, _storage_bump = Pubkey.find_program_address(
        [ingl_constants.PROGRAM_STORAGE_SEED], get_market_program_id()
    )
    escrow_account_key, _escrow_bump = Pubkey.find_program_address(
        [ingl_constants.ESCROW_SEED], get_market_program_id()
    )

    storage_account_data = Storage.parse(
        (await client.get_account_info(storage_account_key)).value.data
    )
    buyer_key = Pubkey(storage_account_data.purchase.buyer)
    assert authorized_withdrawer.pubkey == Pubkey(
        storage_account_data.authorized_withdrawer
    ), "Authorized withdrawer signing is not the same as the one in storage account"

    # Forming AccountMetas
    buyer_meta = AccountMeta(pubkey=buyer_key, is_signer=False, is_writable=True)
    storage_account_meta = AccountMeta(
        pubkey=storage_account_key, is_signer=False, is_writable=True
    )
    escrow_account_meta = AccountMeta(
        pubkey=escrow_account_key, is_signer=False, is_writable=True
    )
    authorized_withdrawer_meta = AccountMeta(
        pubkey=authorized_withdrawer.pubkey, is_signer=True, is_writable=True
    )
    system_program_meta = AccountMeta(
        pubkey=system_program.ID, is_signer=False, is_writable=False
    )

    account_metas = [
        buyer_meta,
        storage_account_meta,
        escrow_account_meta,
        authorized_withdrawer_meta,
        # programs listed below
        system_program_meta,
    ]

    # Forming Transaction
    transaction = Transaction()
    transaction.add(
        build_market_instruction(
            MarketInstructionEnum.enum.ValidateSecondaryItemsTransfers(
                item_index=item_index, log_level=log_level
            ),
            account_metas,
        )
    )

    # Sign Transaction, Send Transaction, and Confirm Transaction, Return Transaction Signature
    return await sign_send_confirm_return_tx_as_link(
        transaction, client, authorized_withdrawer
    )
