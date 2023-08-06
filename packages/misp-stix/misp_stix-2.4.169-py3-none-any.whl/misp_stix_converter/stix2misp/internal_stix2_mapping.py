#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import Mapping
from .stix2_mapping import STIX2toMISPMapping


class InternalSTIX2toMISPMapping(STIX2toMISPMapping):
    def __init__(self):
        super().__init__()
        first_seen_attribute = {'type': 'datetime', 'object_relation': 'first-seen'}
        last_seen_attribute = {'type': 'datetime', 'object_relation': 'last-seen'}
        self._declare_mapping(
            updates = {
                'location': {
                    'x_misp_altitude': {'type': 'float', 'object_relation': 'altitude'},
                    'x_misp_country': {'type': 'text', 'object_relation': 'country'},
                    'x_misp_epsg': {'type': 'text', 'object_relation': 'epsg'},
                    'x_misp_first_seen': first_seen_attribute,
                    'x_misp_last_seen': last_seen_attribute,
                    'x_misp_neighborhood': {'type': 'text', 'object_relation': 'neighborhood'},
                    'x_misp_spacial_reference': {
                        'type': 'text',
                        'object_relation': 'spacial-reference'
                    }
                }
            }
        )
        self.__attributes_mapping = {
            'vulnerability': '_parse_vulnerability_attribute'
        }
        indicator_attributes_mapping = {
            'AS': '_attribute_from_AS',
            'attachment': '_attribute_from_attachment',
            'malware-sample': '_attribute_from_malware_sample'
        }
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'authentihash',
                    'cdhash',
                    'domain',
                    'email',
                    'email-attachment',
                    'email-body',
                    'email-dst',
                    'email-header',
                    'email-message-id',
                    'email-reply-to',
                    'email-src',
                    'email-subject',
                    'email-x-mailer',
                    'filename',
                    'hostname',
                    'http-method',
                    'imphash',
                    'impfuzzy',
                    'link',
                    'mac-address',
                    'md5',
                    'mutex',
                    'pehash',
                    'port',
                    'sha1',
                    'sha224',
                    'sha256',
                    'sha384',
                    'sha512',
                    'sha512/224',
                    'sha512/256',
                    'sha3-224',
                    'sha3-256',
                    'sha3-384',
                    'sha3-512',
                    'size-in-bytes',
                    'ssdeep',
                    'regkey',
                    'telfhash',
                    'tlsh',
                    'uri',
                    'url',
                    'user-agent',
                    'vhash',
                    'x509-fingerprint-md5',
                    'x509-fingerprint-sha1',
                    'x509-fingerprint-sha256'
                ),
                '_attribute_from_simple_pattern'
            )
        )
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'filename|authentihash',
                    'filename|imphash',
                    'filename|impfuzzy',
                    'filename|md5',
                    'filename|pehash',
                    'filename|sha1',
                    'filename|sha224',
                    'filename|sha256',
                    'filename|sha384',
                    'filename|sha512',
                    'filename|sha512/224',
                    'filename|sha512/256',
                    'filename|sha3-224',
                    'filename|sha3-256',
                    'filename|sha3-384',
                    'filename|sha3-512',
                    'filename|ssdeep',
                    'filename|tlsh',
                    'filename|vhash'
                ),
                '_attribute_from_filename_hash'
            )
        )
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'domain|ip',
                    'hostname|port',
                    'regkey|value'
                ),
                '_attribute_from_double_pattern'
            )
        )
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'github-username',
                    'ip-src',
                    'ip-dst'
                ),
                '_attribute_from_dual_pattern'
            )
        )
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'ip-src|port',
                    'ip-dst|port'
                ),
                '_attribute_from_ip_port'
            )
        )
        indicator_attributes_mapping.update(
            dict.fromkeys(
                (
                    'sigma',
                    'snort',
                    'yara'
                ),
                '_attribute_from_patterning_language'
            )
        )
        self.__indicator_attributes_mapping = Mapping(**indicator_attributes_mapping)
        observable_attributes_mapping = {
            'AS': '_attribute_from_AS',
            'attachment': '_attribute_from_attachment',
            'domain': '_attribute_from_domain',
            'domain|ip': '_attribute_from_domain_ip',
            'email-attachment': '_attribute_from_email_attachment',
            'email-body': '_attribute_from_email_body',
            'email-header': '_attribute_from_email_header',
            'email-message-id': '_attribute_from_email_message_id',
            'email-reply-to': '_attribute_from_email_reply_to',
            'email-subject': '_attribute_from_email_subject',
            'email-x-mailer': '_attribute_from_email_x_mailer',
            'github-username': '_attribute_from_github_username',
            'hostname|port': '_attribute_from_hostname_port',
            'malware-sample': '_attribute_from_malware_sample',
            'regkey': '_attribute_from_regkey',
            'regkey|value': '_attribute_from_regkey_value'
        }
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'domain',
                    'email',
                    'hostname',
                    'link',
                    'mac-address',
                    'mutex',
                    'uri',
                    'url'
                ),
                '_attribute_from_first'
            )
        )
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'authentihash',
                    'cdhash',
                    'imphash',
                    'impfuzzy',
                    'md5',
                    'pehash',
                    'sha1',
                    'sha224',
                    'sha256',
                    'sha384',
                    'sha512',
                    'sha512/224',
                    'sha512/256',
                    'sha3-224',
                    'sha3-256',
                    'sha3-384',
                    'sha3-512',
                    'ssdeep',
                    'telfhash',
                    'tlsh',
                    'vhash',
                    'x509-fingerprint-md5',
                    'x509-fingerprint-sha1',
                    'x509-fingerprint-sha256'
                ),
                '_attribute_from_hash'
            )
        )
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'filename|authentihash',
                    'filename|imphash',
                    'filename|impfuzzy',
                    'filename|md5',
                    'filename|pehash',
                    'filename|sha1',
                    'filename|sha224',
                    'filename|sha256',
                    'filename|sha384',
                    'filename|sha512',
                    'filename|sha512/224',
                    'filename|sha512/256',
                    'filename|sha3-224',
                    'filename|sha3-256',
                    'filename|sha3-384',
                    'filename|sha3-512',
                    'filename|ssdeep',
                    'filename|tlsh',
                    'filename|vhash'
                ),
                '_attribute_from_filename_hash'
            )
        )
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'ip-src|port',
                    'ip-dst|port'
                ),
                '_attribute_from_ip_port'
            )
        )
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'filename',
                    'mutex'
                ),
                '_attribute_from_name'
            )
        )
        observable_attributes_mapping.update(
            dict.fromkeys(
                (
                    'email-dst',
                    'email-src',
                    'ip-src',
                    'ip-dst'
                ),
                '_attribute_from_second'
            )
        )
        self.__observable_attributes_mapping = Mapping(**observable_attributes_mapping)
        objects_mapping = {
            'android-app': '_object_from_android_app',
            'asn': '_object_from_asn',
            'attack-pattern': '_parse_attack_pattern_object',
            'course-of-action': '_parse_course_of_action_object',
            'cpe-asset': '_object_from_cpe_asset',
            'credential': '_object_from_credential',
            'domain-ip': '_object_from_domain_ip',
            'email': '_object_from_email',
            'employee': '_parse_employee_object',
            'facebook-account': '_object_from_facebook_account',
            'file': '_object_from_file',
            'geolocation': '_parse_location_object',
            'github-user': '_object_from_github_user',
            'gitlab-user': '_object_from_gitlab_user',
            'http-request': '_object_from_http_request',
            'image': '_object_from_image',
            'ip-port': '_object_from_ip_port',
            'legal-entity': '_parse_legal_entity_object',
            'lnk': '_object_from_lnk',
            'mutex': '_object_from_mutex',
            'netflow': '_object_from_netflow',
            'network-connection': '_object_from_network_connection',
            'network-socket': '_object_from_network_socket',
            'news-agency': '_parse_news_agency_object',
            'organization': '_parse_organization_object',
            'parler-account': '_object_from_parler_account',
            'process': '_object_from_process',
            'reddit-account': '_object_from_reddit_account',
            'registry-key': '_object_from_registry_key',
            'script': '_parse_script_object',
            'telegram-account': '_object_from_telegram_account',
            'twitter-account': '_object_from_twitter_account',
            'url': '_object_from_url',
            'user-account': '_object_from_user_account',
            'vulnerability': '_parse_vulnerability_object',
            'x509': '_object_from_x509'
        }
        objects_mapping.update(
            dict.fromkeys(
                (
                    'sigma',
                    'suricata',
                    'yara'
                ),
                '_object_from_patterning_language'
            )
        )
        self.__objects_mapping = Mapping(**objects_mapping)

        # ATTRIBUTES DECLARATION
        account_id_attribute = {'type': 'text', 'object_relation': 'account-id'}
        account_name_attribute = {'type': 'text', 'object_relation': 'account-name'}
        alias_attribute = {'type': 'text', 'object_relation': 'alias'}
        archive_attribute = {'type': 'link', 'object_relation': 'archive'}
        attachment_attribute = {'type': 'attachment', 'object_relation': 'attachment'}
        authentihash_attribute = {'type': 'authentihash', 'object_relation': 'authentihash'}
        basicauth_password_attribute = {'type': 'text', 'object_relation': 'basicauth-password'}
        basicauth_user_attribute = {'type': 'text', 'object_relation': 'basicauth-user'}
        bcc_attribute = {'type': 'email-dst', 'object_relation': 'bcc'}
        bcc_display_name_attribute = {'type': 'email-dst-display-name', 'object_relation': 'bcc-display-name'}
        bio_attribute = {'type': 'text', 'object_relation': 'bio'}
        byte_count_attribute = {'type': 'counter', 'object_relation': 'byte-count'}
        cc_attribute = {'type': 'email-dst', 'object_relation': 'cc'}
        cc_display_name_attribute = {'type': 'email-dst-display-name', 'object_relation': 'cc-display-name'}
        certificate_attribute = {'type': 'x509-fingerprint-sha1', 'object_relation': 'certificate'}
        comment_text_attribute = {'type': 'text', 'object_relation': 'comment'}
        community_id_attribute = {'type': 'community-id', 'object_relation': 'community-id'}
        compilation_timestamp_attribute = {'type': 'datetime', 'object_relation': 'compilation-timestamp'}
        direction_attribute = {'type': 'text', 'object_relation': 'direction'}
        email_attachment_attribute = {'type': 'email-attachment', 'object_relation': 'attachment'}
        email_header_attribute = {'type': 'email-header', 'object_relation': 'header'}
        eml_attribute = {'type': 'attachment', 'object_relation': 'eml'}
        employee_type_attribute = {'type': 'text', 'object_relation': 'employee-type'}
        fake_process_name_attribute = {'type': 'boolean', 'object_relation': 'fake-process-name'}
        flow_count_attribute = {'type': 'counter', 'object_relation': 'flow-count'}
        followers_attribute = {'type': 'text', 'object_relation': 'followers'}
        following_attribute = {'type': 'text', 'object_relation': 'following'}
        format_attribute = {'type': 'text', 'object_relation': 'format'}
        fullpath_attribute = {'type': 'text', 'object_relation': 'fullpath'}
        from_attribute = {'type': 'email-src', 'object_relation': 'from'}
        from_display_name_attribute = {'type': 'email-src-display-name', 'object_relation': 'from-display-name'}
        from_domain_attribute = {'type': 'domain', 'object_relation': 'from-domain'}
        guid_attribute = {'type': 'text', 'object_relation': 'guid'}
        header_attribute = {'type': 'text', 'object_relation': 'header'}
        hostname_attribute = {'type': 'hostname', 'object_relation': 'hostname'}
        hostname_dst_attribute = {'type': 'hostname', 'object_relation': 'hostname-dst'}
        hostname_src_attribute = {'type': 'hostname', 'object_relation': 'hostname-src'}
        id_attribute = {'type': 'text', 'object_relation': 'id'}
        image_attribute = {'type': 'filename', 'object_relation': 'image'}
        image_text_attribute = {'type': 'text', 'object_relation': 'image-text'}
        integrity_level_attribute = {'type': 'text', 'object_relation': 'integrity-level'}
        ip_protocol_number_attribute = {'type': '', 'object_relation': 'ip-protocol-number'}
        ip_source_attribute = {'type': 'ip-src', 'object_relation': 'ip-src'}
        ip_version_attribute = {'type': 'counter', 'object_relation': 'ip_version'}
        is_ca_attribute = {'type': 'boolean', 'object_relation': 'is_ca'}
        likes_attribute = {'type': 'text', 'object_relation': 'likes'}
        link_attribute = {'type': 'link', 'object_relation': 'link'}
        lnk_access_time_attribute = {'type': 'datetime', 'object_relation': 'lnk-access-time'}
        lnk_creation_time_attribute = {'type': 'datetime', 'object_relation': 'lnk-creation-time'}
        lnk_modification_time_attribute = {'type': 'datetime', 'object_relation': 'lnk-modification-time'}
        mime_boundary_attribute = {'type': 'email-mime-boundary', 'object_relation': 'mime-boundary'}
        msg_attribute = {'type': 'attachment', 'object_relation': 'msg'}
        packet_count_attribute = {'type': 'counter', 'object_relation': 'packet-count'}
        parent_command_line_attribute = {'type': 'text', 'object_relation': 'parent-command-line'}
        parent_guid_attribute = {'type': 'text', 'object_relation': 'parent-guid'}
        parent_image_attribute = {'type': 'filename', 'object_relation': 'parent-image'}
        parent_pid_attribute = {'type': 'text', 'object_relation': 'parent-pid'}
        parent_process_name_attribute = {'type': 'text', 'object_relation': 'parent-process-name'}
        parent_process_path_attribute = {'type': 'text', 'object_relation': 'parent-process-path'}
        pattern_in_file_attribute = {'type': 'pattern-in-file', 'object_relation': 'pattern-in-file'}
        pem_attribute = {'type': 'text', 'object_relation': 'pem'}
        pgid_attribute = {'type': 'text', 'object_relation': 'pgid'}
        port_attribute = {'type': 'port', 'object_relation': 'port'}
        process_state_attribute = {'type': 'process-state', 'object_relation': 'process-state'}
        proxy_password_attribute = {'type': 'text', 'object_relation': 'proxy-password'}
        proxy_user_attribute = {'type': 'text', 'object_relation': 'proxy-user'}
        pubkey_info_size_attribute = {'type': 'text', 'object_relation': 'pubkey-info-size'}
        raw_base64_attribute = {'type': 'text', 'object_relation': 'raw-base64'}
        received_hostname_attribute = {'type': 'hostname', 'object_relation': 'received-header-hostname'}
        received_ip_attribute = {'type': 'ip-src', 'object_relation': 'received-header-ip'}
        reply_to_display_name_attribute = {'type': 'email-dst-display-name', 'object_relation': 'reply-to-display-name'}
        return_path_attribute = {'type': 'email-src', 'object_relation': 'return-path'}
        role_attribute = {'type': 'text', 'object_relation': 'role'}
        screenshot_attribute = {'type': 'attachment', 'object_relation': 'screenshot'}
        script_attribute = {'type': 'text', 'object_relation': 'script'}
        sha224_attribute = {'type': 'sha224', 'object_relation': 'sha224'}
        sha3_224_attribute = {'type': 'sha3-224', 'object_relation': 'sha3-224'}
        sha3_384_attribute = {'type': 'sha3-384', 'object_relation': 'sha3-384'}
        sha384_attribute = {'type': 'sha384', 'object_relation': 'sha384'}
        state_attribute = {'type': 'text', 'object_relation': 'state'}
        start_time_attribute = {'type': 'datetime', 'object_relation': 'start-time'}
        telfhash_attribute = {'type': 'telfhash', 'object_relation': 'telfhash'}
        text_attribute = {'type': 'text', 'object_relation': 'text'}
        thread_index_attribute = {'type': 'email-thread-index', 'object_relation': 'thread-index'}
        to_attribute = {'type': 'email-dst', 'object_relation': 'to'}
        to_display_name_attribute = {'type': 'email-dst-display-name', 'object_relation': 'to-display-name'}
        user_avatar_attribute = {'type': 'attachment', 'object_relation': 'user-avatar'}
        user_creator_attribute = {'type': 'text', 'object_relation': 'user-creator'}
        user_process_attribute = {'type': 'text', 'object_relation': 'user-process'}
        verified_attribute = {'type': 'text', 'object_relation': 'verified'}
        vhash_attribute = {'type': 'vhash', 'object_relation': 'vhash'}
        self.__dst_as_attribute = Mapping(
            **{'type': 'AS', 'object_relation': 'dst-as'}
        )
        self.__icmp_type_attribute = Mapping(
            **{'type': 'text', 'object_relation': 'icmp-type'}
        )
        self.__protocol_attribute = Mapping(
            **{'type': 'text', 'object_relation': 'protocol'}
        )
        self.__src_as_attribute = Mapping(
            **{'type': 'AS', 'object_relation': 'src-as'}
        )
        self.__tcp_flags_attribute = Mapping(
            **{'type': 'text', 'object_relation': 'tcp-flags'}
        )

        # STIX TO MISP OBJECTS MAPPING
        self.__android_app_object_mapping = Mapping(
            name = self.name_attribute,
            x_misp_appid = {'type': 'text', 'object_relation': 'appid'},
            x_misp_certificate = {'type': 'sha1', 'object_relation': 'certificate'},
            x_misp_domain = self.domain_attribute,
            x_misp_sha256 = self.sha256_attribute
        )
        self.__annotation_object_mapping = Mapping(
            content = text_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_creation_date = {'type': 'datetime', 'object_relation': 'creation-date'},
            x_misp_format = format_attribute,
            x_misp_modification_data = {'type': 'datetime', 'object_relation': 'modification-date'},
            x_misp_ref = {'type': 'link', 'object_relation': 'ref'},
            x_misp_type = self.type_attribute
        )
        self.__asn_object_mapping = Mapping(
            number = {'type': 'AS', 'object_relation': 'asn'},
            name = self.description_attribute,
            x_misp_country = {'type': 'text', 'object_relation': 'country'},
            x_misp_export = {'type': 'text', 'object_relation': 'export'},
            x_misp_first_seen = first_seen_attribute,
            x_misp_import = {'type': 'text', 'object_relation': 'import'},
            x_misp_last_seen = last_seen_attribute,
            x_misp_mp_export = {'type': 'text', 'object_relation': 'mp-export'},
            x_misp_mp_import = {'type': 'text', 'object_relation': 'mp-import'},
            x_misp_subnet_announced = {'type': 'ip-src', 'object_relation': 'subnet-announced'}
        )
        self.__attack_pattern_object_mapping = Mapping(
            description = self.summary_attribute,
            name = self.name_attribute,
            x_misp_prerequisites = {'type': 'text', 'object_relation': 'prerequisites'},
            x_misp_related_weakness = {'type': 'weakness', 'object_relation': 'related-weakness'},
            x_misp_solutions = {'type': 'text', 'object_relation': 'solutions'}
        )
        self.__course_of_action_object_mapping = Mapping(
            name = self.name_attribute,
            description = self.description_attribute,
            x_misp_cost = {'type': 'text', 'object_relation': 'cost'},
            x_misp_efficacy = {'type': 'text', 'object_relation': 'efficacy'},
            x_misp_impact = {'type': 'text', 'object_relation': 'impact'},
            x_misp_objective = {'type': 'text', 'object_relation': 'objective'},
            x_misp_stage = {'type': 'text', 'object_relation': 'stage'},
            x_misp_type = self.type_attribute
        )
        self.__cpe_asset_object_mapping = Mapping(
            cpe = self.cpe_attribute,
            languages = self.language_attribute,
            name = {'type': 'text', 'object_relation': 'product'},
            vendor = self.vendor_attribute,
            version = self.version_attribute,
            x_misp_description = self.description_attribute,
            x_misp_other = {'type': 'text', 'object_relation': 'other'},
            x_misp_part = {'type': 'text', 'object_relation': 'part'},
            x_misp_product = {'type': 'text', 'object_relation': 'product'},
            x_misp_sw_edition = {'type': 'text', 'object_relation': 'sw_edition'},
            x_misp_target_hw = {'type': 'text', 'object_relation': 'target_hw'},
            x_misp_target_sw = {'type': 'text', 'object_relation': 'target_sw'},
            x_misp_update = {'type': 'text', 'object_relation': 'update'},
        )
        self.__credential_object_mapping = Mapping(
            user_id = self.username_attribute,
            credential = self.password_attribute,
            x_misp_password = self.password_attribute,
            x_misp_format = format_attribute,
            x_misp_notification = {'type': 'text', 'object_relation': 'notification'},
            x_misp_origin = {'type': 'text', 'object_relation': 'origin'},
            x_misp_text = text_attribute,
            x_misp_type = self.type_attribute
        )
        self.__domain_ip_object_mapping = Mapping(
            value = self.domain_attribute,
            x_misp_first_seen = first_seen_attribute,
            x_misp_hostname = hostname_attribute,
            x_misp_last_seen = last_seen_attribute,
            x_misp_port = port_attribute,
            x_misp_registration_date = {'type': 'datetime', 'object_relation': 'registration-date'},
            x_misp_text = text_attribute
        )
        self.__email_indicator_object_mapping = Mapping(
            **{
                'additional_header_fields.reply_to': self.reply_to_attribute,
                'additional_header_fields.x_mailer': self.x_mailer_attribute,
                'bcc_refs': {
                    'display_name': bcc_display_name_attribute,
                    'value': bcc_attribute
                },
                'body': self.email_body_attribute,
                'cc_refs': {
                    'display_name': cc_display_name_attribute,
                    'value': cc_attribute
                },
                'date': self.send_date_attribute,
                'from_ref.display_name': from_display_name_attribute,
                'from_ref.value': from_attribute,
                'message_id': self.message_id_attribute,
                'subject': self.email_subject_attribute,
                'to_refs': {
                    'display_name': to_display_name_attribute,
                    'value': to_attribute
                },
                'x_misp_attachment': email_attachment_attribute,
                'x_misp_from_domain': from_domain_attribute,
                'x_misp_ip_src': ip_source_attribute,
                'x_misp_message_id': self.message_id_attribute,
                'x_misp_mime_boundary': mime_boundary_attribute,
                'x_misp_received_header_hostname': received_hostname_attribute,
                'x_misp_received_header_ip': received_ip_attribute,
                'x_misp_reply_to_display_name': reply_to_display_name_attribute,
                'x_misp_return_path': return_path_attribute,
                'x_misp_screenshot': screenshot_attribute,
                'x_misp_thread_index': thread_index_attribute,
                'x_misp_user_agent': self.user_agent_attribute
            }
        )
        self.__email_object_mapping = Mapping(
            body = self.email_body_attribute,
            date = self.send_date_attribute,
            message_id = self.message_id_attribute,
            subject = self.email_subject_attribute,
            x_misp_attachment = email_attachment_attribute,
            x_misp_from_domain = from_domain_attribute,
            x_misp_ip_src = ip_source_attribute,
            x_misp_message_id = self.message_id_attribute,
            x_misp_mime_boundary = mime_boundary_attribute,
            x_misp_received_header_hostname = received_hostname_attribute,
            x_misp_received_header_ip = received_ip_attribute,
            x_misp_reply_to_display_name = reply_to_display_name_attribute,
            x_misp_return_path = return_path_attribute,
            x_misp_screenshot = screenshot_attribute,
            x_misp_thread_index = thread_index_attribute,
            x_misp_user_agent = self.user_agent_attribute
        )
        self.__employee_object_mapping = Mapping(
            name = {'type': 'full-name', 'object_relation': 'full-name'},
            description = {'type': 'text', 'object_relation': 'text'},
            roles = employee_type_attribute,
            x_misp_business_unit = {'type': 'target-org', 'object_relation': 'business_unit'},
            x_misp_employee_type = employee_type_attribute,
            x_misp_first_name = {'type': 'first-name', 'object_relation': 'first-name'},
            x_misp_last_name = {'type': 'last-name', 'object_relation': 'last-name'},
            x_misp_primary_asset = {'type': 'target-machine', 'object_relation': 'primary-asset'},
            x_misp_userid = {'type': 'target-user', 'object_relation': 'userid'}
        )
        self.__facebook_account_object_mapping = Mapping(
            user_id = account_id_attribute,
            account_login = account_name_attribute,
            x_misp_archive = archive_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_description = self.description_attribute,
            x_misp_link = link_attribute,
            x_misp_url = self.url_attribute,
            x_misp_user_avatar = user_avatar_attribute
        )
        self.__file_hashes_object_mapping = Mapping(
            **{
                'AUTHENTIHASH': authentihash_attribute,
                'IMPHASH': self.imphash_attribute,
                'MD5': self.md5_attribute,
                'SHA1': self.sha1_attribute,
                'SHA-1': self.sha1_attribute,
                'SHA224': sha224_attribute,
                'SHA256': self.sha256_attribute,
                'SHA-256': self.sha256_attribute,
                'SHA3224': sha3_224_attribute,
                'SHA3-256': self.sha3_256_attribute,
                'SHA3384': sha3_384_attribute,
                'SHA3-512': self.sha3_512_attribute,
                'SHA384': sha384_attribute,
                'SHA512': self.sha512_attribute,
                'SHA-512': self.sha512_attribute,
                'ssdeep': self.ssdeep_attribute,
                'SSDEEP': self.ssdeep_attribute,
                'TELFHASH': telfhash_attribute,
                'TLSH': self.tlsh_attribute,
                'VHASH': vhash_attribute
            }
        )
        self.__file_indicator_object_mapping = Mapping(
            **{
                'hashes.AUTHENTIHASH': authentihash_attribute,
                'hashes.IMPHASH': self.imphash_attribute,
                'hashes.MD5': self.md5_attribute,
                'hashes.SHA1': self.sha1_attribute,
                'hashes.SHA224': sha224_attribute,
                'hashes.SHA256': self.sha256_attribute,
                'hashes.SHA3224': sha3_224_attribute,
                'hashes.SHA3256': self.sha3_256_attribute,
                'hashes.SHA3384': sha3_384_attribute,
                'hashes.SHA3512': self.sha3_512_attribute,
                'hashes.SHA384': sha384_attribute,
                'hashes.SHA512': self.sha512_attribute,
                'hashes.SSDEEP': self.ssdeep_attribute,
                'hashes.TELFHASH': telfhash_attribute,
                'hashes.TLSH': self.tlsh_attribute,
                'hashes.VHASH': vhash_attribute,
                'mime_type': self.mime_type_attribute,
                'name': self.filename_attribute,
                'name_enc': self.file_encoding_attribute,
                'parent_directory_ref.path': self.path_attribute,
                'size': self.size_in_bytes_attribute,
                'x_misp_certificate': certificate_attribute,
                'x_misp_compilation_timestamp': compilation_timestamp_attribute,
                'x_misp_entropy': self.entropy_attribute,
                'x_misp_fullpath': fullpath_attribute,
                'x_misp_path': self.path_attribute,
                'x_misp_pattern_in_file': pattern_in_file_attribute,
                'x_misp_state': state_attribute,
                'x_misp_text': text_attribute
            }
        )
        self.__file_observable_object_mapping = Mapping(
            accessed = self.access_time_attribute,
            atime = self.access_time_attribute,
            created = self.creation_time_attribute,
            ctime = self.creation_time_attribute,
            mime_type = self.mime_type_attribute,
            modified = self.modification_time_attribute,
            mtime = self.modification_time_attribute,
            name = self.filename_attribute,
            name_enc = self.file_encoding_attribute,
            size = self.size_in_bytes_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_certificate = certificate_attribute,
            x_misp_compilation_timestamp = compilation_timestamp_attribute,
            x_misp_entropy = self.entropy_attribute,
            x_misp_fullpath = fullpath_attribute,
            x_misp_path = self.path_attribute,
            x_misp_pattern_in_file = pattern_in_file_attribute,
            x_misp_state = state_attribute,
            x_misp_text = text_attribute
        )
        self.__github_user_object_mapping = Mapping(
            user_id = id_attribute,
            account_login = {'type': 'github-username', 'object_relation': 'username'},
            display_name = {'type': 'text', 'object_relation': 'user-fullname'},
            x_misp_avatar_url = {'type': 'link', 'object_relation': 'avatar_url'},
            x_misp_bio = bio_attribute,
            x_misp_blog = {'type': 'text', 'object_relation': 'blog'},
            x_misp_company = {'type': 'text', 'object_relation': 'company'},
            x_misp_follower = {'type': 'github-username', 'object_relation': 'follower'},
            x_misp_following = {'type': 'github-username', 'object_relation': 'following'},
            x_misp_link = link_attribute,
            x_misp_location = {'type': 'text', 'object_relation': 'location'},
            x_misp_node_id = {'type': 'text', 'object_relation': 'node_id'},
            x_misp_organisation = {'type': 'github-organisation', 'object_relation': 'organisation'},
            x_misp_profile_image = {'type': 'attachment', 'object_relation': 'profile-image'},
            x_misp_public_gists = {'type': 'text', 'object_relation': 'public_gists'},
            x_misp_public_repos = {'type': 'text', 'object_relation': 'public_repos'},
            x_misp_repository = {'type': 'github-repository', 'object_relation': 'repository'},
            x_misp_twitter_username = {'type': 'text', 'object_relation': 'twitter_username'},
            x_misp_verified = verified_attribute
        )
        self.__gitlab_user_object_mapping = Mapping(
            user_id = id_attribute,
            display_name = self.name_attribute,
            account_login = self.username_attribute,
            x_misp_avatar_url = {'type': 'link', 'object_relation': 'avatar_url'},
            x_misp_state = {'type': 'text', 'object_relation': 'state'},
            x_misp_web_url = {'type': 'link', 'object_relation': 'web_url'}
        )
        self.__http_request_extension_mapping = Mapping(
            request_method = self.method_attribute,
            request_value = self.uri_attribute
        )
        self.__http_request_header_mapping = Mapping(
            **{
                'Content-Type': self.content_type_attribute,
                'Cookie': self.cookie_attribute,
                'Referer': self.referer_attribute,
                'User-Agent': self.user_agent_attribute
            }
        )
        self.__http_request_object_mapping = Mapping(
            x_misp_basicauth_password = basicauth_password_attribute,
            x_misp_basicauth_user = basicauth_user_attribute,
            x_misp_header = header_attribute,
            x_misp_proxy_password = proxy_password_attribute,
            x_misp_proxy_user = proxy_user_attribute,
            x_misp_text = text_attribute,
            x_misp_url = self.url_attribute
        )
        http_ext = "extensions.'http-request-ext'"
        self.__http_request_pattern_object_mapping = Mapping(
            **{
                f"{http_ext}.request_method": self.method_attribute,
                f"{http_ext}.request_header.'Content-Type'": self.content_type_attribute,
                f"{http_ext}.request_header.'Cookie'": self.cookie_attribute,
                f"{http_ext}.request_header.'Referer'": self.referer_attribute,
                f"{http_ext}.request_header.'User-Agent'": self.user_agent_attribute,
                'x_misp_basicauth_password': basicauth_password_attribute,
                'x_misp_basicauth_user': basicauth_user_attribute,
                'x_misp_header': header_attribute,
                'x_misp_proxy_password': proxy_password_attribute,
                'x_misp_proxy_user': proxy_user_attribute,
                'x_misp_text': text_attribute,
            }
        )
        self.__image_indicator_object_mapping = Mapping(
            **{
                'name': self.filename_attribute,
                'content_ref.url': self.url_attribute,
                'content_ref.x_misp_url': self.url_attribute,
                'x_misp_archive': archive_attribute,
                'x_misp_image_text': image_text_attribute,
                'x_misp_link': link_attribute,
                'x_misp_username': self.username_attribute
            }
        )
        self.__image_observable_object_mapping = Mapping(
            name = self.filename_attribute,
            x_misp_archive = archive_attribute,
            x_misp_image_text = image_text_attribute,
            x_misp_link = link_attribute,
            x_misp_username = self.username_attribute
        )
        self.__ip_port_object_mapping = Mapping(
            dst_port = self.dst_port_attribute,
            src_port = self.src_port_attribute,
            start = first_seen_attribute,
            end = last_seen_attribute,
            x_misp_AS = {'type': 'AS', 'object_relation': 'AS'},
            x_misp_country_code = {'type': 'text', 'object_relation': 'country-code'},
            x_misp_domain = self.domain_attribute,
            x_misp_hostname = hostname_attribute,
            x_misp_ip = self.ip_attribute,
            x_misp_text = text_attribute
        )
        self.__legal_entity_contact_information_mapping = Mapping(
            **{
                'phone-number': {'type': 'phone-number'},
                'website': {'type': 'link'}
            }
        )
        self.__legal_entity_object_mapping = Mapping(
            name = self.name_attribute,
            description = text_attribute,
            sectors = {'type': 'text', 'object_relation': 'business'},
            x_misp_commercial_name = {'type': 'text', 'object_relation': 'commercial-name'},
            x_misp_legal_form = {'type': 'text', 'object_relation': 'legal-form'},
            x_misp_registration_number = {'type': 'text', 'object_relation': 'registration-number'}
        )
        __lnk_indicator_object_mapping = {
            'hashes.MD5': self.md5_attribute,
            'hashes.SHA1': self.sha1_attribute,
            'hashes.SHA224': sha224_attribute,
            'hashes.SHA256': self.sha256_attribute,
            'hashes.SHA384': sha384_attribute,
            'hashes.SHA512': self.sha512_attribute,
            'hashes.SSDEEP': self.ssdeep_attribute,
            'hashes.TLSH': self.tlsh_attribute,
            'parent_directory_ref.path': self.path_attribute
        }
        __lnk_object_mapping = Mapping(
            name = self.filename_attribute,
            accessed = lnk_access_time_attribute,
            atime = lnk_access_time_attribute,
            created = lnk_creation_time_attribute,
            ctime = lnk_creation_time_attribute,
            modified = lnk_modification_time_attribute,
            mtime = lnk_modification_time_attribute,
            size = self.size_in_bytes_attribute,
            x_misp_fullpath = fullpath_attribute,
            x_misp_path = self.path_attribute,
            x_misp_birth_droid_file_identifier = {'type': 'text', 'object_relation': 'birth-droid-file-identifier'},
            x_misp_birth_droid_volume_identifier = {'type': 'text', 'object_relation': 'birth-droid-volume-identifier'},
            x_misp_droid_file_identifier = {'type': 'text', 'object_relation': 'droid-file-identifier'},
            x_misp_droid_volume_identifier = {'type': 'text', 'object_relation': 'droid-volume-identifier'},
            x_misp_entropy = self.entropy_attribute,
            x_misp_lnk_command_line_arguments = {'type': 'text', 'object_relation': 'lnk-command-line-arguments'},
            x_misp_lnk_description = {'type': 'text', 'object_relation': 'lnk-description'},
            x_misp_lnk_drive_serial_number = {'type': 'text', 'object_relation': 'lnk-drive-serial-number'},
            x_misp_lnk_drive_type = {'type': 'text', 'object_relation': 'lnk-drive-type'},
            x_misp_lnk_file_attribute_flags = {'type': 'text', 'object_relation': 'lnk-file-attribute-flags'},
            x_misp_lnk_file_size = {'type': 'size-in-bytes', 'object_relation': 'lnk-file-size'},
            x_misp_lnk_hot_key_value = {'type': 'text', 'object_relation': 'lnk-hot-key-value'},
            x_misp_lnk_icon_text = {'type': 'text', 'object_relation': 'lnk-icon-text'},
            x_misp_lnk_local_path = {'type': 'text', 'object_relation': 'lnk-local-path'},
            x_misp_lnk_relative_path = {'type': 'text', 'object_relation': 'lnk-relative-path'},
            x_misp_lnk_show_window_value = {'type': 'text', 'object_relation': 'lnk-show-window-value'},
            x_misp_lnk_volume_label = {'type': 'text', 'object_relation': 'lnk-volume-label'},
            x_misp_lnk_working_directory = {'type': 'text', 'object_relation': 'lnk-working-directory'},
            x_misp_machine_identifier = {'type': 'text', 'object_relation': 'machine-identifier'},
            x_misp_pattern_in_file = pattern_in_file_attribute,
            x_misp_state = state_attribute,
            x_misp_text = text_attribute
        )
        __lnk_indicator_object_mapping.update(__lnk_object_mapping)
        self.__lnk_indicator_object_mapping = Mapping(**__lnk_indicator_object_mapping)
        self.__lnk_observable_object_mapping = __lnk_object_mapping
        self.__mutex_object_mapping = Mapping(
            name = self.name_attribute,
            x_misp_description = self.description_attribute,
            x_misp_operating_system = {'type': 'text', 'object_relation': 'operating-system'}
        )
        self.__netflow_object_mapping = Mapping(
            dst_port = self.dst_port_attribute,
            src_port = self.src_port_attribute,
            start = self.first_packet_seen_attribute,
            end = self.last_packet_seen_attribute,
            src_byte_count = byte_count_attribute,
            src_packets = packet_count_attribute,
            x_misp_community_id = community_id_attribute,
            x_misp_direction = direction_attribute,
            x_misp_flow_count = flow_count_attribute,
            x_misp_ip_protocol_number = ip_protocol_number_attribute,
            x_misp_ip_version = ip_version_attribute
        )
        self.__netflow_pattern_object_mapping = Mapping(
            **{
                'dst_port': self.dst_port_attribute,
                'src_port': self.src_port_attribute,
                'start': self.first_packet_seen_attribute,
                'end': self.last_packet_seen_attribute,
                'src_byte_count': byte_count_attribute,
                'src_packets': packet_count_attribute,
                'protocols[0]': self.protocol_attribute,
                "extensions.'icmp-ext'.icmp_type_hex": self.icmp_type_attribute,
                "extensions.'tcp-ext'.src_flags_hex": self.tcp_flags_attribute,
                'x_misp_community_id': community_id_attribute,
                'x_misp_direction': direction_attribute,
                'x_misp_flow_count': flow_count_attribute,
                'x_misp_ip_protocol_number': ip_protocol_number_attribute,
                'x_misp_ip_version': ip_version_attribute
            }
        )
        self.__network_connection_object_mapping = Mapping(
            dst_port = self.dst_port_attribute,
            src_port = self.src_port_attribute,
            start = self.first_packet_seen_attribute,
            x_misp_community_id = community_id_attribute,
            x_misp_hostname_dst = hostname_dst_attribute,
            x_misp_hostname_src = hostname_src_attribute
        )
        self.__network_socket_object_mapping = Mapping(
            dst_port = self.dst_port_attribute,
            src_port = self.src_port_attribute,
            x_misp_address_family = self.address_family_attribute,
            x_misp_domain_family = self.domain_family_attribute,
            x_misp_filename = self.filename_attribute,
            x_misp_hostname_dst = hostname_dst_attribute,
            x_misp_hostname_src = hostname_src_attribute,
            x_misp_option = {'type': 'text', 'object_relation': 'option'}
        )
        self.__news_agency_contact_information_mapping = Mapping(
            **{
                'address': {'type': 'text'},
                'e-mail': {'type': 'email-src'},
                'fax-number': {'type': 'phone-number'},
                'link': {'type': 'link'},
                'phone-number': {'type': 'phone-number'}
            }
        )
        self.__news_agency_object_mapping = Mapping(
            name = self.name_attribute,
            x_misp_alias = alias_attribute,
            x_misp_archive = archive_attribute,
            x_misp_url = self.url_attribute
        )
        self.__organization_contact_information_mapping = Mapping(
            **{
                'address': {'type': 'text'},
                'e-mail': {'type': 'email-src'},
                'fax-number': {'type': 'phone-number'},
                'phone-number': {'type': 'phone-number'}
            }
        )
        self.__organization_object_mapping = Mapping(
            name = self.name_attribute,
            description = self.description_attribute,
            roles = role_attribute,
            x_misp_role = role_attribute,
            x_misp_alias = alias_attribute,
            x_misp_date_of_inception = {
                'type': 'datetime',
                'object_relation': 'date-of-inception'
            },
            x_misp_type_of_organization = {
                'type': 'text',
                'object_relation': 'type-of-organization'
            },
            x_misp_VAT = {'type': 'text', 'object_relation': 'VAT'}
        )
        self.__parent_process_object_mapping = Mapping(
            command_line = parent_command_line_attribute,
            name = parent_process_name_attribute,
            x_misp_process_name = parent_process_name_attribute,
            pid = parent_pid_attribute,
            x_misp_guid = parent_guid_attribute,
            x_misp_process_path = parent_process_path_attribute
        )
        self.__parler_account_object_mapping = Mapping(
            user_id = account_id_attribute,
            account_login = account_name_attribute,
            x_misp_archive = archive_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_badge = {'type': 'link', 'object_relation': 'badge'},
            x_misp_bio = bio_attribute,
            x_misp_comments = {'type': 'text', 'object_relation': 'comments'},
            x_misp_cover_photo = {'type': 'attachment', 'object_relation': 'cover-photo'},
            x_misp_followers = followers_attribute,
            x_misp_following = following_attribute,
            x_misp_human = {'type': 'boolean', 'object_relation': 'human'},
            x_misp_interactions = {'type': 'float', 'object_relation': 'interactions'},
            x_misp_likes = likes_attribute,
            x_misp_link = link_attribute,
            x_misp_posts = {'type': 'text', 'object_relation': 'posts'},
            x_misp_profile_photo = {'type': 'attachment', 'object_relation': 'profile-photo'},
            x_misp_url = self.url_attribute,
            x_misp_verified = {'type': 'boolean', 'object_relation': 'verified'},
        )
        self.__pe_object_mapping = Mapping(
            imphash = self.imphash_attribute,
            number_of_sections = self.number_of_sections_attribute,
            pe_type = self.type_attribute,
            x_misp_authentihash = authentihash_attribute,
            x_misp_company_name = {'type': 'text', 'object_relation': 'company-name'},
            x_misp_compilation_timestamp = compilation_timestamp_attribute,
            x_misp_entrypoint_section_at_position = {
                'type': 'text',
                'object_relation': 'entrypoint-section-at-position'
            },
            x_misp_file_description = {'type': 'text', 'object_relation': 'file-description'},
            x_misp_file_version = {'type': 'text', 'object_relation': 'file-version'},
            x_misp_impfuzzy = {'type': 'impfuzzy', 'object_relation': 'impfuzzy'},
            x_misp_internal_filename = {'type': 'filename', 'object_relation': 'internal-filename'},
            x_misp_lang_id = {'type': 'text', 'object_relation': 'lang-id'},
            x_misp_legal_copyright = {'type': 'text', 'object_relation': 'legal-copyright'},
            x_misp_original_filename = {'type': 'filename', 'object_relation': 'original-filename'},
            x_misp_pehash = {'type': 'pehash', 'object_relation': 'pehash'},
            x_misp_product_name = {'type': 'text', 'object_relation': 'product-name'},
            x_misp_product_version = {'type': 'text', 'object_relation': 'product-version'},
            x_misp_richpe = {'type': 'md5', 'object_relation': 'richpe'},
            x_misp_text = text_attribute
        )
        self.__pe_section_object_mapping = Mapping(
            entropy = self.entropy_attribute,
            name = self.name_attribute,
            size = self.size_in_bytes_attribute,
            x_misp_characteristic = {'type': 'text', 'object_relation': 'characteristic'},
            x_misp_offset = {'type': 'hex', 'object_relation': 'offset'},
            x_misp_text = text_attribute,
            x_misp_virtual_address = {'type': 'hex', 'object_relation': 'virtual_address'},
            x_misp_virtual_size = {'type': 'size-in-bytes', 'object_relation': 'virtual_size'}
        )
        self.__process_indicator_object_mapping = Mapping(
            **{
                'arguments': self.args_attribute,
                'command_line': self.command_line_attribute,
                'created': self.creation_time_attribute,
                'created_time': self.creation_time_attribute,
                'cwd': self.current_directory_attribute,
                'is_hidden': self.hidden_attribute,
                'name': self.name_attribute,
                'binary_ref.name': image_attribute,
                'image_ref.name': image_attribute,
                'parent_ref.command_line': parent_command_line_attribute,
                'parent_ref.name': parent_process_name_attribute,
                'parent_ref.pid': parent_pid_attribute,
                'parent_ref.binary_ref.name': parent_image_attribute,
                'parent_ref.image_ref.name': parent_image_attribute,
                'parent_ref.x_misp_guid': parent_guid_attribute,
                'parent_ref.x_misp_process_name': parent_process_name_attribute,
                'parent_ref.x_misp_process_path': parent_process_path_attribute,
                'pid': self.pid_attribute,
                'x_misp_args': self.args_attribute,
                'x_misp_fake_process_name': fake_process_name_attribute,
                'x_misp_guid': guid_attribute,
                'x_misp_integrity_level': integrity_level_attribute,
                'x_misp_name': self.name_attribute,
                'x_misp_pgid': pgid_attribute,
                'x_misp_port': port_attribute,
                'x_misp_process_state': process_state_attribute,
                'x_misp_start_time': start_time_attribute,
                'x_misp_user_creator': user_creator_attribute,
                'x_misp_user_process': user_process_attribute
            }
        )
        self.__process_observable_object_mapping = Mapping(
            arguments = self.args_attribute,
            x_misp_args = self.args_attribute,
            command_line = self.command_line_attribute,
            created = self.creation_time_attribute,
            created_time = self.creation_time_attribute,
            cwd = self.current_directory_attribute,
            is_hidden = self.hidden_attribute,
            name = self.name_attribute,
            x_misp_name = self.name_attribute,
            pid = self.pid_attribute,
            x_misp_fake_process_name = fake_process_name_attribute,
            x_misp_guid = guid_attribute,
            x_misp_integrity_level = integrity_level_attribute,
            x_misp_pgid = pgid_attribute,
            x_misp_port = port_attribute,
            x_misp_process_state = process_state_attribute,
            x_misp_start_time = start_time_attribute,
            x_misp_user_creator = user_creator_attribute,
            x_misp_user_process = user_process_attribute
        )
        self.__reddit_account_object_mapping = Mapping(
            user_id = account_id_attribute,
            account_login = account_name_attribute,
            x_misp_account_avatar = {'type': 'attachment', 'object_relation': 'account-avatar'},
            x_misp_account_avatar_url = {'type': 'url', 'object_relation': 'account-avatar-url'},
            x_misp_archive = archive_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_description = self.description_attribute,
            x_misp_link = link_attribute,
            x_misp_moderator_of = {'type': '', 'object_relation': 'moderator-of'},
            x_misp_trophies = {'type': '', 'object_relation': 'trophies'},
            x_misp_url = self.url_attribute
        )
        self.__registry_key_object_mapping = Mapping(
            key = self.regkey_attribute,
            modified = self.last_modified_attribute,
            modified_time = self.last_modified_attribute,
            x_misp_hive = {'type': 'text', 'object_relation': 'hive'},
            x_misp_root_keys = {'type': 'text', 'object_relation': 'root-keys'}
        )
        self.__script_from_malware_object_mapping = Mapping(
            name = self.filename_attribute,
            description = comment_text_attribute,
            implementation_languages = self.language_attribute,
            x_misp_script = script_attribute,
            x_misp_state = state_attribute
        )
        self.__script_from_tool_object_mapping = Mapping(
            name = self.filename_attribute,
            description = comment_text_attribute,
            x_misp_language = self.language_attribute,
            x_misp_script = script_attribute,
            x_misp_state = state_attribute
        )
        self.__sigma_object_mapping = Mapping(
            pattern = self.sigma_attribute,
            description = self.comment_attribute,
            name = self.sigma_rule_name_attribute,
            x_misp_context = {'type': 'text', 'object_relation': 'context'}
        )
        self.__telegram_account_object_mapping = Mapping(
            user_id = id_attribute,
            account_login = self.username_attribute,
            x_misp_first_name = {'type': 'text', 'object_relation': 'first_name'},
            x_misp_last_name = {'type': 'text', 'object_relation': 'last_name'},
            x_misp_phone = {'type': 'text', 'object_relation': 'phone'},
            x_misp_verified = {'type': 'text', 'object_relation': 'verified'}
        )
        self.__twitter_account_object_mapping = Mapping(
            user_id = id_attribute,
            account_login = self.name_attribute,
            display_name = {'type': 'text', 'object_relation': 'displayed-name'},
            x_misp_archive = archive_attribute,
            x_misp_attachment = attachment_attribute,
            x_misp_bio = bio_attribute,
            x_misp_description = self.description_attribute,
            x_misp_embedded_link = {'type': 'url', 'object_relation': 'embedded-link'},
            x_misp_embedded_safe_link = {'type': 'link', 'object_relation': 'embedded-safe-link'},
            x_misp_followers = followers_attribute,
            x_misp_following = following_attribute,
            x_misp_hashtag = {'type': 'text', 'object_relation': 'hashtag'},
            x_misp_joined_date = {'type': 'text', 'object_relation': 'joined-date'},
            x_misp_likes = likes_attribute,
            x_misp_link = link_attribute,
            x_misp_listed = {'type': 'text', 'object_relation': 'listed'},
            x_misp_location = {'type': 'text', 'object_relation': 'location'},
            x_misp_media = {'type': 'text', 'object_relation': 'media'},
            x_misp_private = {'type': 'text', 'object_relation': 'private'},
            x_misp_profile_banner = {'type': 'attachment', 'object_relation': 'profile-banner'},
            x_misp_profile_banner_url = {'type': 'url', 'object_relation': 'profile-banner-url'},
            x_misp_profile_image = {'type': 'attachment', 'object_relation': 'profile-image'},
            x_misp_profile_image_url = {'type': 'url', 'object_relation': 'profile-image-url'},
            x_misp_tweets = {'type': 'text', 'object_relation': 'tweets'},
            x_misp_twitter_followers = {'type': 'text', 'object_relation': 'twitter-followers'},
            x_misp_twitter_following = {'type': 'text', 'object_relation': 'twitter-following'},
            x_misp_url = self.url_attribute,
            x_misp_verified = verified_attribute
        )
        self.__url_object_mapping = Mapping(
            value = self.url_attribute,
            x_misp_credential = {'type': 'text', 'object_relation': 'credential'},
            x_misp_domain = self.domain_attribute,
            x_misp_domain_without_tld = {'type': 'text', 'object_relation': 'domain_without_tld'},
            x_misp_first_seen = first_seen_attribute,
            x_misp_fragment = {'type': 'text', 'object_relation': 'fragment'},
            x_misp_host = {'type': 'hostname', 'object_relation': 'host'},
            x_misp_ip = self.ip_attribute,
            x_misp_last_seen = last_seen_attribute,
            x_misp_port = port_attribute,
            x_misp_query_string = {'type': 'text', 'object_relation': 'query_string'},
            x_misp_resource_path = {'type': 'text', 'object_relation': 'resource_path'},
            x_misp_scheme = {'type': 'text', 'object_relation': 'scheme'},
            x_misp_subdomain = {'type': 'text', 'object_relation': 'subdomain'},
            x_misp_text = text_attribute,
            x_misp_tld = {'type': 'text', 'object_relation': 'tld'}
        )
        self.__user_account_object_mapping = Mapping(
            account_login = self.username_attribute,
            account_type = self.account_type_attribute,
            can_escalate_privs = self.can_escalate_privs_attribute,
            credential = self.password_attribute,
            x_misp_password = self.password_attribute,
            display_name = self.display_name_attribute,
            is_disabled = self.disabled_attribute,
            is_privileged = self.privileged_attribute,
            is_service_account = self.is_service_account_attribute,
            user_id = self.user_id_attribute,
            x_misp_description = self.description_attribute,
            x_misp_link = link_attribute,
            x_misp_user_avatar = user_avatar_attribute,
            account_created = self.created_attribute,
            account_expires = self.expires_attribute,
            account_first_login = self.first_login_attribute,
            account_last_login = self.last_login_attribute,
            credential_last_changed = self.password_last_changed_attribute,
            password_last_changed = self.password_last_changed_attribute
        )
        self.__vulnerability_object_mapping = Mapping(
            description = self.description_attribute,
            x_misp_created = {'type': 'datetime', 'object_relation': 'created'},
            x_misp_credit = {'type': 'text', 'object_relation': 'credit'},
            x_misp_cvss_score = {'type': 'float', 'object_relation': 'cvss-score'},
            x_misp_modified = {'type': 'datetime', 'object_relation': 'modified'},
            x_misp_published = {'type': 'datetime', 'object_relation': 'published'},
            x_misp_state = {'type': 'text', 'object_relation': 'state'},
            x_misp_summary = self.summary_attribute,
            x_misp_vulnerable_configuration = {
                'type': 'cpe',
                'object_relation': 'vulnerable-configuration'
            }
        )
        self.__x509_indicator_object_mapping = Mapping(
            **{
                'hashes.MD5': self.x509_md5_attribute,
                'hashes.SHA1': self.x509_sha1_attribute,
                'hashes.SHA256': self.x509_sha256_attribute,
                'is_self_signed': self.is_self_signed_attribute,
                'issuer': self.issuer_attribute,
                'serial_number': self.serial_number_attribute,
                'signature_algorithm': self.signature_algorithm_attribute,
                'subject': self.subject_attribute,
                'subject_public_key_algorithm': self.pubkey_info_algorithm_attribute,
                'subject_public_key_exponent': self.pubkey_info_exponent_attribute,
                'subject_public_key_modulus': self.pubkey_info_modulus_attribute,
                'validity_not_after': self.validity_not_after_attribute,
                'validity_not_before': self.validity_not_before_attribute,
                'version': self.version_attribute,
                'x_misp_is_ca': is_ca_attribute,
                'x_misp_pem': pem_attribute,
                'x_misp_pubkey_info_size': pubkey_info_size_attribute,
                'x_misp_raw_base64': raw_base64_attribute,
                'x_misp_text': text_attribute
            }
        )
        self.__x509_observable_object_mapping = Mapping(
            is_self_signed = self.is_self_signed_attribute,
            issuer = self.issuer_attribute,
            serial_number = self.serial_number_attribute,
            signature_algorithm = self.signature_algorithm_attribute,
            subject = self.subject_attribute,
            subject_public_key_algorithm = self.pubkey_info_algorithm_attribute,
            subject_public_key_exponent = self.pubkey_info_exponent_attribute,
            subject_public_key_modulus = self.pubkey_info_modulus_attribute,
            validity_not_after = self.validity_not_after_attribute,
            validity_not_before = self.validity_not_before_attribute,
            version = self.version_attribute,
            x_misp_is_ca = is_ca_attribute,
            x_misp_pem = pem_attribute,
            x_misp_pubkey_info_size = pubkey_info_size_attribute,
            x_misp_raw_base64 = raw_base64_attribute,
            x_misp_text = text_attribute
        )
        self.__x509_subject_alternative_name_mapping = Mapping(
            **{
                'DNS name': {'type': 'hostname', 'object_relation': 'dns_names'},
                'email': {'type': 'email-dst', 'object_relation': 'email'},
                'IP': self.ip_attribute,
                'RID': {'type': 'text', 'object_relation': 'rid'},
                'URI': self.uri_attribute
            }
        )
        self.__yara_object_mapping = Mapping(
            pattern = self.yara_attribute,
            description = self.comment_attribute,
            name = self.yara_rule_name_attribute,
            pattern_version = self.version_attribute,
            x_misp_context = {'type': 'text', 'object_relation': 'context'}
        )

    @property
    def android_app_object_mapping(self) -> dict:
        return self.__android_app_object_mapping

    @property
    def annotation_object_mapping(self) -> dict:
        return self.__annotation_object_mapping

    @property
    def asn_object_mapping(self) -> dict:
        return self.__asn_object_mapping

    @property
    def attack_pattern_object_mapping(self) -> dict:
        return self.__attack_pattern_object_mapping

    @property
    def attributes_mapping(self) -> dict:
        return self.__attributes_mapping

    @property
    def course_of_action_object_mapping(self) -> dict:
        return self.__course_of_action_object_mapping

    @property
    def cpe_asset_object_mapping(self) -> dict:
        return self.__cpe_asset_object_mapping

    @property
    def credential_object_mapping(self) -> dict:
        return self.__credential_object_mapping

    @property
    def domain_ip_object_mapping(self) -> dict:
        return self.__domain_ip_object_mapping

    @property
    def dst_as_attribute(self) -> dict:
        return self.__dst_as_attribute

    @property
    def email_indicator_object_mapping(self) -> dict:
        return self.__email_indicator_object_mapping

    @property
    def email_object_mapping(self) -> dict:
        return self.__email_object_mapping

    @property
    def employee_object_mapping(self) -> dict:
        return self.__employee_object_mapping

    @property
    def facebook_account_object_mapping(self) -> dict:
        return self.__facebook_account_object_mapping

    @property
    def file_hashes_object_mapping(self) -> dict:
        return self.__file_hashes_object_mapping

    @property
    def file_indicator_object_mapping(self) -> dict:
        return self.__file_indicator_object_mapping

    @property
    def file_observable_object_mapping(self) -> dict:
        return self.__file_observable_object_mapping

    @property
    def github_user_object_mapping(self) -> dict:
        return self.__github_user_object_mapping

    @property
    def gitlab_user_object_mapping(self) -> dict:
        return self.__gitlab_user_object_mapping

    @property
    def http_request_extension_mapping(self) -> dict:
        return self.__http_request_extension_mapping

    @property
    def http_request_header_mapping(self) -> dict:
        return self.__http_request_header_mapping

    @property
    def http_request_object_mapping(self) -> dict:
        return self.__http_request_object_mapping

    @property
    def http_request_pattern_object_mapping(self) -> dict:
        return self.__http_request_pattern_object_mapping

    @property
    def icmp_type_attribute(self) -> dict:
        return self.__icmp_type_attribute

    @property
    def image_indicator_object_mapping(self) -> dict:
        return self.__image_indicator_object_mapping

    @property
    def image_observable_object_mapping(self) -> dict:
        return self.__image_observable_object_mapping

    @property
    def indicator_attributes_mapping(self) -> dict:
        return self.__indicator_attributes_mapping

    @property
    def ip_port_object_mapping(self) -> dict:
        return self.__ip_port_object_mapping

    @property
    def legal_entity_contact_information_mapping(self) -> dict:
        return self.__legal_entity_contact_information_mapping

    @property
    def legal_entity_object_mapping(self) -> dict:
        return self.__legal_entity_object_mapping

    @property
    def lnk_indicator_object_mapping(self) -> dict:
        return self.__lnk_indicator_object_mapping

    @property
    def lnk_observable_object_mapping(self) -> dict:
        return self.__lnk_observable_object_mapping

    @property
    def mutex_object_mapping(self) -> dict:
        return self.__mutex_object_mapping

    @property
    def netflow_object_mapping(self) -> dict:
        return self.__netflow_object_mapping

    @property
    def netflow_pattern_object_mapping(self) -> dict:
        return self.__netflow_pattern_object_mapping

    @property
    def network_connection_object_mapping(self) -> dict:
        return self.__network_connection_object_mapping

    @property
    def network_socket_object_mapping(self) -> dict:
        return self.__network_socket_object_mapping

    @property
    def news_agency_object_mapping(self) -> dict:
        return self.__news_agency_object_mapping

    @property
    def news_agency_contact_information_mapping(self) -> dict:
        return self.__news_agency_contact_information_mapping

    @property
    def objects_mapping(self) -> dict:
        return self.__objects_mapping

    @property
    def observable_attributes_mapping(self) -> dict:
        return self.__observable_attributes_mapping

    @property
    def organization_object_mapping(self) -> dict:
        return self.__organization_object_mapping

    @property
    def organization_contact_information_mapping(self) -> dict:
        return self.__organization_contact_information_mapping

    @property
    def parent_process_object_mapping(self) -> dict:
        return self.__parent_process_object_mapping

    @property
    def parler_account_object_mapping(self) -> dict:
        return self.__parler_account_object_mapping

    @property
    def pe_object_mapping(self) -> dict:
        return self.__pe_object_mapping

    @property
    def pe_section_object_mapping(self) -> dict:
        return self.__pe_section_object_mapping

    @property
    def process_indicator_object_mapping(self) -> dict:
        return self.__process_indicator_object_mapping

    @property
    def process_observable_object_mapping(self) -> dict:
        return self.__process_observable_object_mapping

    @property
    def protocol_attribute(self) -> dict:
        return self.__protocol_attribute

    @property
    def reddit_account_object_mapping(self) -> dict:
        return self.__reddit_account_object_mapping

    @property
    def registry_key_object_mapping(self) -> dict:
        return self.__registry_key_object_mapping

    @property
    def script_from_malware_object_mapping(self) -> dict:
        return self.__script_from_malware_object_mapping

    @property
    def script_from_tool_object_mapping(self) -> dict:
        return self.__script_from_tool_object_mapping

    @property
    def sigma_object_mapping(self) -> dict:
        return self.__sigma_object_mapping

    @property
    def src_as_attribute(self) -> dict:
        return self.__src_as_attribute

    @property
    def tcp_flags_attribute(self) -> dict:
        return self.__tcp_flags_attribute

    @property
    def telegram_account_object_mapping(self) -> dict:
        return self.__telegram_account_object_mapping

    @property
    def twitter_account_object_mapping(self) -> dict:
        return self.__twitter_account_object_mapping

    @property
    def url_object_mapping(self) -> dict:
        return self.__url_object_mapping

    @property
    def user_account_object_mapping(self) -> dict:
        return self.__user_account_object_mapping

    @property
    def vulnerability_object_mapping(self) -> dict:
        return self.__vulnerability_object_mapping

    @property
    def x509_indicator_object_mapping(self) -> dict:
        return self.__x509_indicator_object_mapping

    @property
    def x509_observable_object_mapping(self) -> dict:
        return self.__x509_observable_object_mapping

    @property
    def x509_subject_alternative_name_mapping(self) -> dict:
        return self.__x509_subject_alternative_name_mapping

    @property
    def yara_object_mapping(self) -> dict:
        return self.__yara_object_mapping
