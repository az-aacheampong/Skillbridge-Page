window.dash_clientside = window.dash_clientside || {};

window.dash_clientside.addDropZone = {
    dropZoneGrid2GridSimple: async function (gridIdLeft, gridIdRight) {
        // Get the grids APIs
        const gridLeftAPI = await dash_ag_grid.getApiAsync(gridIdLeft);
        const gridRightAPI = await dash_ag_grid.getApiAsync(gridIdRight);

        // Get the dropzones parameters from the RIGHT grid
        const gridRightDropZone = gridRightAPI.getRowDropZoneParams();

        // Add RIGHT grid as dropzone of LEFT grid only
        gridLeftAPI.addRowDropZone(gridRightDropZone);

        return window.dash_clientside.no_update;
    },
}



// window.dash_clientside = window.dash_clientside || {};

// window.dash_clientside.addDropZone = {
//     dropZoneGrid2GridSimple: async function(gridIdLeft, gridIdRight, dragStopIndicatorId) {
//         const gridLeftAPI = await dash_ag_grid.getApiAsync(gridIdLeft);
//         const gridRightAPI = await dash_ag_grid.getApiAsync(gridIdRight);

//         const dropZoneParams = gridRightAPI.getRowDropZoneParams({
//             onDragStop: function(params) {
//                 // Update a hidden Div's value to trigger a Dash callback
//                 const dragStopIndicator = document.getElementById(dragStopIndicatorId);
//                 dragStopIndicator.textContent = new Date().getTime();  // Use current timestamp as a trigger
//             },
//         });

//         gridLeftAPI.addRowDropZone(dropZoneParams);
//     },
// };


// window.dash_clientside = window.dash_clientside || {};

// window.dash_clientside.addDropZone = {
//     dropZoneGrid2GridSimple: async function (gridIdLeft, gridIdRight, dropCounterId) {
//         const gridLeftAPI = await dash_ag_grid.getApiAsync(gridIdLeft);
//         const gridRightAPI = await dash_ag_grid.getApiAsync(gridIdRight);

//         const gridRightDropZone = gridRightAPI.getRowDropZoneParams({
//             onDragStop: function(params) {
//                 const dropCounterElement = document.getElementById(dropCounterId);
//                 let count = parseInt(dropCounterElement.textContent) || 0;
//                 dropCounterElement.textContent = count + 1;
//             }
//         });

//         gridLeftAPI.addRowDropZone(gridRightDropZone);

//         return window.dash_clientside.no_update;
//     },
// };

// Get the Grid API
// const gridAPI = await dash_ag_grid.getApiAsync(gridId)

// // Define the Drop Zone
// const targetContainer = document.querySelector('.target-container');

// const dropZoneParams = {
//     // Function that returns the DropZone HTMLElement.
//     getContainer: () => targetContainer,
//     // Function that will be executed when the rowDrag enters the target.
//     onDragEnter: params => {
//         console.log('DropZone entered')
//     },
//     // Function that will be executed when the rowDrag leaves the target
//     onDragLeave: params => {
//         console.log('DropZone left')
//     },
//     // Function that will be executed when the rowDrag is dragged inside the target.
//     // Note: this gets called multiple times.
//     onDragging: params => {
//         console.log('Dragging inside the DropZone')
//     },
//     // Function that will be executed when the rowDrag drops rows within the target.
//     onDragStop: params => {
//         // Update the hidden div with relevant data, such as the row data
//         const hiddenDiv = document.getElementById('hidden-div-for-drag');
//         hiddenDiv.innerHTML = JSON.stringify(params.node.data);
//     }
// }

// // Register the Drop Zone
// gridAPI.addRowDropZone(dropZoneParams);

// // Deregister the Drop Zone when it is no longer required
// gridAPI.removeRowDropZone(dropZoneParams);