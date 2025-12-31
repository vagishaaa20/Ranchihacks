// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceChain {

    struct Evidence {
        string caseId;
        string evidenceId;
        string hash;
        uint256 timestamp;
    }

    mapping(string => Evidence) private evidenceRecords;

    event EvidenceAdded(string evidenceId, string hash);

    function addEvidence(
        string memory _caseId,
        string memory _evidenceId,
        string memory _hash
    ) public {
        evidenceRecords[_evidenceId] = Evidence(
            _caseId,
            _evidenceId,
            _hash,
            block.timestamp
        );

        emit EvidenceAdded(_evidenceId, _hash);
    }

    function getEvidenceHash(string memory _evidenceId)
        public
        view
        returns (string memory)
    {
        return evidenceRecords[_evidenceId].hash;
    }
}
